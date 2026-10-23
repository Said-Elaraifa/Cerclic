"""Cerclic in macOS: the « Cerclic » Quick Action of the Finder's right-click
menu, and opening at login.

Both are plain files in the user's Library, rewritten when Cerclic starts so
they always point to where Cerclic.app is now:
  ~/Library/Services/Cerclic.workflow      the Quick Action (Automator format):
                                            it hands the selected files to
                                            Cerclic, which opens the wheel
  ~/Library/LaunchAgents/<bundle id>.plist  opening at login, in the background

Files also reach Cerclic through « Ouvrir avec » and by being dropped on its
icon: macOS sends them as "open documents" events (see app.py).
"""
from __future__ import annotations

import os
import plistlib
import shlex
import shutil
import subprocess
import sys
import uuid

from ..log import log

BUNDLE_ID = "com.jannahmarketing.cerclic"
SERVICE_NAME = "Cerclic"
PBS = "/System/Library/CoreServices/pbs"
AUTOMATION_SETTINGS = ("x-apple.systempreferences:com.apple.preference.security"
                       "?Privacy_Automation")


def app_bundle() -> str | None:
    """The Cerclic.app running now, None when running from the sources."""
    if not getattr(sys, "frozen", False):
        return None
    exe = os.path.realpath(sys.executable)        # …/Cerclic.app/Contents/MacOS/Cerclic
    app = os.path.dirname(os.path.dirname(os.path.dirname(exe)))
    return app if app.endswith(".app") else None


def _library(*parts: str) -> str:
    return os.path.join(os.path.expanduser("~"), "Library", *parts)


def workflow_path() -> str:
    return _library("Services", f"{SERVICE_NAME}.workflow")


def launch_agent_path() -> str:
    return _library("LaunchAgents", f"{BUNDLE_ID}.plist")


def _write_if_changed(path: str, data: bytes) -> bool:
    try:
        with open(path, "rb") as f:
            if f.read() == data:
                return False
    except OSError:
        pass
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)
    return True


# ----- the Quick Action ------------------------------------------------------------------

def quick_action_command(app: str) -> str:
    """The shell script of the Quick Action: the selected files, as arguments,
    are opened with Cerclic (found by its path, else by its identifier)."""
    return (f"APP={shlex.quote(app)}\n"
            '/usr/bin/open -a "$APP" "$@" 2>/dev/null || '
            f'/usr/bin/open -b {BUNDLE_ID} "$@"\n')


def _service_info() -> dict:
    return {"NSServices": [{
        "NSBackgroundColorName": "background",
        "NSIconName": "NSActionTemplate",
        "NSMenuItem": {"default": SERVICE_NAME},
        "NSMessage": "runWorkflowAsService",
        "NSRequiredContext": {"NSApplicationIdentifier": "com.apple.finder"},
        # images, PDF, videos and sounds (the unusual formats are declared by
        # Cerclic.app, see UTImportedTypeDeclarations in cerclic_mac.spec)
        "NSSendFileTypes": ["public.image", "com.adobe.pdf", "public.movie",
                            "public.audio", "public.audiovisual-content"],
    }]}


def _uuid(name: str) -> str:
    """Stable identifiers: the workflow is only rewritten when it changes."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"cerclic:{name}")).upper()


def _workflow(command: str) -> dict:
    """document.wflow: one "Run Shell Script" action, input passed as arguments,
    shown for files in the Finder (as Automator writes a Quick Action)."""
    def arg(n: int, name: str, default) -> dict:
        return {"default value": default, "name": name, "required": "0", "type": "0",
                "uuid": str(n)}

    action = {
        "AMAccepts": {"Container": "List", "Optional": True,
                      "Types": ["com.apple.cocoa.string"]},
        "AMActionVersion": "2.0.3",
        "AMApplication": ["Automator"],
        "AMParameterProperties": {"COMMAND_STRING": {}, "CheckedForUserDefaultShell": {},
                                  "inputMethod": {}, "shell": {}, "source": {}},
        "AMProvides": {"Container": "List", "Types": ["com.apple.cocoa.string"]},
        "ActionBundlePath": "/System/Library/Automator/Run Shell Script.action",
        "ActionName": "Run Shell Script",
        "ActionParameters": {"COMMAND_STRING": command, "CheckedForUserDefaultShell": True,
                             "inputMethod": 1, "shell": "/bin/zsh", "source": ""},
        "BundleIdentifier": "com.apple.RunShellScript",
        "CFBundleVersion": "2.0.3",
        "CanShowSelectedItemsWhenRun": False,
        "CanShowWhenRun": True,
        "Category": ["AMCategoryUtilities"],
        "Class Name": "RunShellScriptAction",
        "InputUUID": _uuid("input"),
        "Keywords": ["Shell", "Script", "Command", "Run", "Unix"],
        "OutputUUID": _uuid("output"),
        "UUID": _uuid("action"),
        "UnlocalizedApplications": ["Automator"],
        "arguments": {"0": arg(0, "inputMethod", 0),
                      "1": arg(1, "CheckedForUserDefaultShell", False),
                      "2": arg(2, "source", ""),
                      "3": arg(3, "COMMAND_STRING", ""),
                      "4": arg(4, "shell", "/bin/sh")},
        "isViewVisible": 1,
        "location": "309.000000:253.000000",
        "nibPath": "/System/Library/Automator/Run Shell Script.action/Contents/Resources/"
                   "Base.lproj/main.nib",
    }
    return {
        "AMApplicationBuild": "523",
        "AMApplicationVersion": "2.10",
        "AMDocumentVersion": "2",
        "actions": [{"action": action, "isViewVisible": 1}],
        "connectors": {},
        "workflowMetaData": {
            "applicationBundleIDsByPath": {},
            "applicationPaths": [],
            "inputTypeIdentifier": "com.apple.Automator.fileSystemObject",
            "outputTypeIdentifier": "com.apple.Automator.nothing",
            "presentationMode": 15,
            "processesInput": 0,
            "serviceApplicationBundleID": "com.apple.finder",
            "serviceApplicationPath": "/System/Library/CoreServices/Finder.app",
            "serviceInputTypeIdentifier": "com.apple.Automator.fileSystemObject",
            "serviceOutputTypeIdentifier": "com.apple.Automator.nothing",
            "serviceProcessesInput": 0,
            "systemImageName": "NSActionTemplate",
            "useAutomaticInputType": 0,
            "workflowTypeIdentifier": "com.apple.Automator.servicesMenu",
        },
    }


def refresh_services() -> None:
    """Have macOS read the Quick Actions again (else: at the next login)."""
    if os.path.exists(PBS):
        try:
            subprocess.Popen([PBS, "-flush"], stdin=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError:
            pass


def quick_action_installed() -> bool:
    return os.path.isfile(os.path.join(workflow_path(), "Contents", "document.wflow"))


def install_quick_action(app: str | None = None) -> bool:
    """Write the Quick Action, or bring it up to date. True when it changed."""
    app = app or app_bundle()
    if not app:
        return False
    contents = os.path.join(workflow_path(), "Contents")
    changed = _write_if_changed(os.path.join(contents, "Info.plist"),
                                plistlib.dumps(_service_info()))
    changed |= _write_if_changed(os.path.join(contents, "document.wflow"),
                                 plistlib.dumps(_workflow(quick_action_command(app))))
    if changed:
        log("action rapide « Cerclic » installée dans le Finder")
        refresh_services()
    return changed


def remove_quick_action() -> None:
    path = workflow_path()
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
        refresh_services()


# ----- opening at login ----------------------------------------------------------------------

def set_autostart(enabled: bool, app: str | None = None) -> None:
    path = launch_agent_path()
    if not enabled:
        if os.path.exists(path):
            os.remove(path)
        return
    app = app or app_bundle()
    if not app:
        return
    _write_if_changed(path, plistlib.dumps({
        "Label": BUNDLE_ID,
        "AssociatedBundleIdentifiers": [BUNDLE_ID],   # listed as Cerclic in Login Items
        # Cerclic itself, not /usr/bin/open: macOS names the program in its
        # « activité en arrière-plan » notice, which then says « Cerclic »
        "ProgramArguments": [os.path.join(app, "Contents", "MacOS", "Cerclic"), "--background"],
        "RunAtLoad": True,
        "LimitLoadToSessionType": "Aqua",
        "ProcessType": "Interactive",
    }))


def is_autostart() -> bool:
    return os.path.exists(launch_agent_path())


# ----- the rest ------------------------------------------------------------------------------

def open_automation_settings() -> None:
    """System Settings, Privacy & Security, Automation (Cerclic and the Finder)."""
    try:
        subprocess.Popen(["/usr/bin/open", AUTOMATION_SETTINGS])
    except OSError:
        pass


def cleanup() -> None:
    """Take Cerclic out of macOS (before Cerclic.app goes to the Trash)."""
    remove_quick_action()
    try:
        set_autostart(False)
    except OSError:
        pass
