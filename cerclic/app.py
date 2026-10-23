"""The resident Cerclic: tray icon, request server, wheel, editors and jobs.

Flow: a request arrives (right-click entry through the pipe, or the keyboard
shortcut) -> the wheel opens at the cursor -> the chosen action gathers what it
needs (password, text, crop frame, signature placement) in Cerclic's own
windows -> it runs on a worker thread -> a card shows progress, then the result.
"""
from __future__ import annotations

import os
import sys
import threading
import time

from PySide6.QtCore import (QEvent, QEventLoop, QObject, QPoint, QRect, QSize, Qt, QTimer,
                            Signal, qInstallMessageHandler)
from PySide6.QtGui import QCursor
from PySide6.QtNetwork import QLocalServer
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QWidget

from . import APP_NAME, __version__, engine, launcher
from .actions import registry
from .log import log, log_exception, log_path
from .paths import clean_selection, fallback_folder, kind_of, natural_key
from .settings import Settings
from .system import FILES_APP, IS_MAC, IS_WINDOWS, MOD_KEY, OS_NAME, hotkey_supported, hotkeys
from .win.foreground import bring_to_front

# A right-click on many files starts one forwarder per file: paths arriving
# less than MERGE_GAP s after the previous one join the wheel already open.
# When Cerclic was busy as they came (first start, a heavy preview), they
# arrive later in a bunch: a wheel nobody has touched yet still takes them
# for MERGE_UNTOUCHED s.
MERGE_GAP = 1.0
MERGE_UNTOUCHED = 6.0
MERGE_MAX = 60.0


def _gc_now() -> None:
    import gc
    if not gc.isenabled():
        gc.collect()


def _summary(paths: list[str]) -> str:
    if len(paths) == 1:
        name = os.path.basename(paths[0])
        return name if len(name) <= 26 else name[:23] + "…"
    return f"{len(paths)} fichiers"


def _drop_precomputed(opts: dict) -> None:
    """A result the compression popup already made, not wanted after all."""
    for made in (opts.get("precomputed") or {}).values():
        try:
            os.remove(made)
            os.rmdir(os.path.dirname(made))
        except OSError:
            pass


def _elsewhere_note(sources: list[str], outputs: list[str], chosen: str | None = None) -> str:
    """Say so when results could not go where they should: next to the
    original (protected folder), or in the chosen folder (gone)."""
    if not sources or not outputs:
        return ""
    if chosen:
        base = os.path.normcase(os.path.abspath(chosen))
        if all(os.path.normcase(os.path.abspath(o)).startswith(base + os.sep)
               for o in outputs):
            return ""
    folders = {os.path.normcase(os.path.dirname(os.path.abspath(s))) for s in sources}

    def beside(out: str) -> bool:
        out = os.path.normcase(os.path.abspath(out))
        for d in folders:
            try:
                if os.path.commonpath([d, out]) == d:
                    return True
            except ValueError:          # another drive
                pass
        return False

    if all(beside(o) for o in outputs):
        return "Le dossier choisi est introuvable : enregistré à côté de l'original." \
            if chosen else ""
    fb = fallback_folder()
    where = os.path.basename(fb.rstrip("\\/")) or fb
    where = {"downloads": "Téléchargements"}.get(where.lower(), where)  # as Explorer shows it
    return f"Enregistré dans «\u00a0{where}\u00a0» : le dossier d'origine est protégé."


# ----- request server ---------------------------------------------------------------

class RequestServer(QObject):
    """Receives requests from later launches (see launcher.py)."""
    request = Signal(str, list)

    def __init__(self, name: str):
        super().__init__()
        self.server = QLocalServer(self)
        self.server.setSocketOptions(QLocalServer.UserAccessOption)
        if os.name != "nt":
            QLocalServer.removeServer(name)
        self.ok = self.server.listen(name)
        if not self.ok:
            log(f"serveur local indisponible : {self.server.errorString()}")
        self.server.newConnection.connect(self._on_connection)
        self._live: dict = {}

    def _on_connection(self) -> None:
        while self.server.hasPendingConnections():
            sock = self.server.nextPendingConnection()
            buf = bytearray()
            self._live[sock] = buf
            sock.readyRead.connect(lambda s=sock: self._read(s))
            sock.disconnected.connect(lambda s=sock: self._drop(s))
            QTimer.singleShot(5000, lambda s=sock: self._timeout(s))
            if sock.bytesAvailable():
                self._read(sock)

    def _read(self, sock) -> None:
        buf = self._live.get(sock)
        if buf is None:
            return
        buf += bytes(sock.readAll())
        if b"\nEND\n" not in buf:
            if len(buf) > 4_000_000:
                sock.abort()
            return
        parsed = launcher.decode(bytes(buf))
        self._live.pop(sock, None)
        try:
            sock.write(b"OK\n")
            sock.flush()
            sock.disconnectFromServer()
        except RuntimeError:
            pass
        if parsed:
            self.request.emit(parsed[0], parsed[1])

    def _drop(self, sock) -> None:
        self._live.pop(sock, None)
        try:
            sock.deleteLater()
        except RuntimeError:
            pass

    def _timeout(self, sock) -> None:
        if sock in self._live:
            self._live.pop(sock, None)
            try:
                sock.abort()
            except RuntimeError:
                pass


QUIT_WINDOW_TITLE = "Cerclic.Quit"


class _QuitWindow(QWidget):
    """Invisible window the installer closes (WM_CLOSE) to stop Cerclic
    cleanly, without having to start any program."""

    def __init__(self, on_close):
        super().__init__(None, Qt.Tool | Qt.FramelessWindowHint)
        self.setWindowTitle(QUIT_WINDOW_TITLE)
        self._on_close = on_close
        self.winId()        # create the native window, never shown

    def closeEvent(self, e):
        e.ignore()
        QTimer.singleShot(0, self._on_close)


class Bridge(QObject):
    """Signals emitted from other threads, delivered on the GUI thread."""
    hotkey = Signal()
    hotkey_status = Signal(int, bool)     # (registration number, ok)
    selection = Signal(int, list)
    finder_refused = Signal(int)          # macOS: not allowed to ask the Finder
    startup_state = Signal(str, bool)     # Store version: (task state, asked by the user)


class FileOpenApp(QApplication):
    """macOS sends the files of the Finder's Quick Action, of « Ouvrir avec » and
    of a drop on Cerclic's icon as FileOpen events to the application, one per
    file. They are kept until Cerclic is ready (`on_file` set), then handed over."""

    def __init__(self, argv):
        super().__init__(argv)
        self.early_files: list[str] = []
        self.on_file = None

    def event(self, e):
        if e.type() == QEvent.FileOpen:
            path = e.file() or e.url().toLocalFile()
            if path:
                if self.on_file is not None:
                    self.on_file(path)
                else:
                    self.early_files.append(path)
            return True
        return super().event(e)


class Job(QObject):
    progress = Signal(object, str)
    done = Signal(object)
    _ids = 0

    def __init__(self, action_id: str, paths: list[str], opts: dict, journal=None):
        super().__init__()
        Job._ids += 1
        self.id = f"{os.getpid()}-{Job._ids}"
        self.action_id, self.paths, self.opts = action_id, paths, opts
        self.journal = journal
        self.cancel_event = threading.Event()
        self.finished = False

    def start(self) -> None:
        threading.Thread(target=self._run, daemon=True, name="cerclic-job").start()

    def _run(self) -> None:
        from . import jobs
        from .journal import set_current_job
        set_current_job(self.id)
        try:
            res = jobs.run_job(
                self.action_id, self.paths, self.opts,
                on_progress=lambda f, t: self.progress.emit(f, t),
                cancel=self.cancel_event,
                on_reserved=(lambda p: self.journal.add(self.id, p)) if self.journal else None)
        except BaseException as exc:  # never lose the card
            log_exception("tâche")
            res = engine.Result(self.action_id, False, [], engine.friendly_error(exc))
        finally:
            set_current_job(None)
            if self.journal:
                self.journal.finish(self.id)
        try:
            self.done.emit(res)
        except RuntimeError:
            pass


# ----- the wheel session --------------------------------------------------------------

class WheelSession:
    def __init__(self, app: "CerclicApp", paths: list[str], pos: QPoint, source: str):
        from .ui.radial import Wheel
        self.app, self.paths, self.pos, self.source = app, paths, pos, source
        self.created = self.last_add = time.monotonic()
        self._keys = {os.path.normcase(p) for p in paths}
        self._refresh_pending = False
        self.closed = False
        menu = registry.menu_for(paths)
        self.wheel = Wheel(menu, registry.count_by_category(paths), _summary(paths),
                           preview=paths[0] if paths else None)
        self.wheel.chosen.connect(self._chosen)
        self.wheel.cancelled.connect(self.close)
        self.wheel.popup_at(pos)
        self.last_add = time.monotonic()        # building the wheel may take a moment
        log("roue ouverte : " + ", ".join(menu.keys()) + f" ({len(paths)} fichier(s))")

    def can_merge(self) -> bool:
        if self.closed or self.source != "menu" or self.wheel.navigated:
            return False
        now = time.monotonic()
        if now - self.created >= MERGE_MAX:
            return False
        return (now - self.last_add < MERGE_GAP
                or (not self.wheel.touched and now - self.created < MERGE_UNTOUCHED))

    def add(self, paths: list[str]) -> None:
        """Merge already-cleaned paths. The wheel is refreshed once per burst,
        not once per file, so even a big selection merges in no time."""
        self.last_add = time.monotonic()
        grew = False
        for p in paths:
            key = os.path.normcase(p)
            if key not in self._keys:
                self._keys.add(key)
                self.paths.append(p)
                grew = True
        if grew and not self._refresh_pending:
            self._refresh_pending = True
            QTimer.singleShot(30, self._refresh)

    def _refresh(self) -> None:
        self._refresh_pending = False
        if self.closed:
            return
        self.paths.sort(key=lambda p: (natural_key(p), p.lower()))
        try:
            self.wheel.set_menu(registry.menu_for(self.paths),
                                registry.count_by_category(self.paths),
                                _summary(self.paths))
        except RuntimeError:
            pass

    def _chosen(self, action_id: str, opts: dict) -> None:
        self.close(chosen=True)
        self.paths.sort(key=lambda p: (natural_key(p), p.lower()))
        self.app.start_action(action_id, self.paths, opts, self.pos)

    def close(self, chosen: bool = False) -> None:
        if self.closed:
            return
        self.closed = True
        try:
            if self.wheel.isVisible():
                self.wheel.cancel()
        except RuntimeError:
            pass
        if self.app.session is self:
            self.app.session = None
        if not chosen:
            self.app.focus_back_later()


# ----- application ----------------------------------------------------------------------

class CerclicApp(QObject):
    def __init__(self, qapp: QApplication):
        super().__init__()
        from .ui.cards import CardStack
        self.qapp = qapp
        from .settings import config_path, import_classic_settings, is_packaged, is_portable
        self.portable = is_portable()
        self.packaged = is_packaged()       # the Microsoft Store version
        # (the choices made in the classic version, if any, are applied once)
        self._imported = self.packaged and import_classic_settings()
        if self._imported:
            log("réglages repris de la version classique de Cerclic")
        first_run = not os.path.exists(config_path())
        self.settings = Settings.load()
        if first_run and self.portable:
            # The portable version adds nothing to Windows unless asked to
            # (its folder may be deleted at any time). Its settings live
            # beside it, apart from an installed Cerclic's.
            self.settings.set("context_menu", False)
            self.settings.set("autostart", False)
            self.settings.save()
        self.cards = CardStack()
        self._recover_unfinished()
        self.session: WheelSession | None = None
        self._live: set = set()           # editors, bubbles, jobs kept alive
        self._settings_win = None
        self._reading_selection = 0     # number of the read in progress (0: none)
        self._reading_since = 0.0
        self._reads = 0
        self.hotkey = None
        self.hotkey_ok = None
        self._hotkey_paused = False
        self._hk_serial = 0             # number of the latest registration
        self._good_combo = None         # the last combination Windows accepted
        self._trying = None             # set while a newly chosen one is tried
        self._hotkey_note = ""

        self.bridge = Bridge()
        self.bridge.hotkey.connect(self._on_hotkey, Qt.QueuedConnection)
        self.bridge.hotkey_status.connect(self._on_hotkey_status, Qt.QueuedConnection)
        self.bridge.selection.connect(self._on_selection, Qt.QueuedConnection)
        self.bridge.finder_refused.connect(self._on_finder_refused, Qt.QueuedConnection)
        self.bridge.startup_state.connect(self._on_startup_state, Qt.QueuedConnection)

        self.server = RequestServer(launcher.server_name())
        self.server.request.connect(self.handle_request)
        # The installer closes this hidden window to stop Cerclic (Windows; the
        # Store version is stopped by Windows itself, and must not be stopped by
        # the classic version's installer).
        self._quit_window = _QuitWindow(self.quit) if IS_WINDOWS and not self.packaged else None
        # Files sent by macOS (Quick Action, Ouvrir avec, drop on the icon).
        self.files_received = False
        self._opened: list[str] = []
        self._opened_timer = QTimer(self, singleShot=True, interval=150)
        self._opened_timer.timeout.connect(self._open_received)
        if isinstance(qapp, FileOpenApp):
            qapp.on_file = self._file_opened
            for path in qapp.early_files:
                self._file_opened(path)
            qapp.early_files.clear()
        self._build_tray()
        self.apply_integration()
        if self.packaged:
            QTimer.singleShot(1500, self._check_package)

    # -- interrupted actions -------------------------------------------------------------
    def _recover_unfinished(self) -> None:
        """Remove what an abruptly stopped previous run left half-written, then
        note every path the coming actions reserve until they finish."""
        from . import paths as _paths
        from .journal import Journal, current_job
        from .settings import config_dir
        self.journal = Journal(os.path.join(config_dir(), "pending.json"))
        for p in self.journal.recover():
            log(f"fichier inachevé retiré : {p}")
        _paths.add_reserve_hook(lambda p: self.journal.add(current_job(), p))
        try:                       # sizes worked out by compression popups closed in a hurry
            from .ui.compress_editor import clean_stale
            clean_stale()
        except Exception:
            log_exception("nettoyage des fichiers temporaires")

    # -- tray ------------------------------------------------------------------------
    def _build_tray(self) -> None:
        from .ui.trayicon import make_tray_icon
        self.tray = QSystemTrayIcon(make_tray_icon(), self.qapp)
        self.tray.setToolTip(f"{APP_NAME} {__version__}")
        menu = QMenu()
        menu.addAction("Ouvrir Cerclic", self.open_settings)
        menu.addSeparator()
        menu.addAction("Quitter Cerclic", self.quit)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._tray_activated)
        self.tray.show()
        self._menu = menu

    def _tray_activated(self, reason) -> None:
        if IS_MAC:
            return              # a click on the menu bar icon shows its menu
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.open_settings()

    # -- integration -------------------------------------------------------------------
    def apply_integration(self) -> None:
        """Right-click entry, start with Windows and the shortcut, as set."""
        self._apply_shell()
        self._apply_hotkey()

    def _apply_shell(self, changed: str | None = None) -> None:
        if os.environ.get("CERCLIC_NO_INTEGRATION"):   # tests: leave the system alone
            return
        if IS_MAC:
            self._apply_mac()
        if self.packaged:
            self._apply_package(changed)
        elif os.name == "nt":
            from .win import shell
            # (The portable version only ever removes what points to itself:
            # an installed Cerclic keeps its entries.)
            try:
                if self.settings.get("context_menu"):
                    if not shell.context_menu_ok():
                        shell.install_context_menu()
                        log("entrée « Cerclic » ajoutée au clic droit")
                elif not self.portable or shell.context_menu_mine():
                    shell.remove_context_menu()
            except Exception:
                log_exception("clic droit : échec de l'installation")
            try:
                if self.settings.get("autostart"):
                    shell.set_autostart(True)
                elif not self.portable or shell.is_autostart():
                    shell.set_autostart(False)
            except Exception:
                log_exception("démarrage avec Windows : échec")

    # -- Microsoft Store version ------------------------------------------------------
    def _apply_package(self, changed: str | None = None) -> None:
        """Inside the package nothing goes to the registry: the right-click entry
        (CerclicMenu.dll) reads a marker, starting with Windows is the package's
        startup task (read, or changed when the user asks, away from the window)."""
        from .win import package
        if changed in (None, "context_menu"):
            try:
                package.set_menu(bool(self.settings.get("context_menu")))
            except Exception:
                log_exception("clic droit du paquet")
        if changed in (None, "autostart"):
            # At start Windows' state is read (the user may have changed it in
            # Task Manager); the first time, a choice taken from the classic
            # version is applied instead.
            apply = changed is not None or self._imported
            self._imported = False
            want = bool(self.settings.get("autostart")) if apply else None

            def work():
                try:
                    state = (package.startup_state() if want is None
                             else package.set_startup(want))
                except Exception:
                    log_exception("tâche de démarrage du paquet")
                    state = None
                try:
                    self.bridge.startup_state.emit(state or "", want is not None)
                except RuntimeError:
                    pass
            threading.Thread(target=work, daemon=True, name="cerclic-startup").start()

    def _on_startup_state(self, state: str, asked: bool) -> None:
        if not state:
            return                      # unknown (no answer): leave things as they are
        from .win import package
        on = package.startup_on(state)
        wanted = bool(self.settings.get("autostart"))
        if wanted != on:
            self.settings.set("autostart", on)
            self.settings.save()
        win = self._settings_window()
        if win is not None:
            try:
                win.set_autostart(on)
            except RuntimeError:
                pass
        if asked and wanted and not on:
            if state == "disabled_by_policy":
                self.message("Lancement avec Windows bloqué",
                             "Ton organisation ne permet pas aux applications de se lancer "
                             "avec Windows.", kind="warn")
            else:
                self.message("Lancement avec Windows désactivé dans Windows",
                             "Il a été désactivé dans le Gestionnaire des tâches : seul "
                             "Windows peut le réactiver. Dans Paramètres, Applications, "
                             "Démarrage, active « Cerclic ».", kind="warn",
                             buttons=[("Plus tard", None),
                                      ("Ouvrir", package.open_startup_settings)],
                             auto_ms=20000)
        log(f"lancement avec Windows : {state}")

    def _check_package(self) -> None:
        from .win import package
        package.clean_open_lists()
        if not package.classic_installed():
            return
        log("la version classique de Cerclic est aussi installée")
        uninstaller = package.classic_uninstaller()
        if uninstaller:
            from .ui.cards import reveal_path
            self.message("Deux Cerclic installés",
                         "La version de Cerclic installée sans le Microsoft Store est "
                         "encore là. Pour n'avoir qu'un « Cerclic » dans le clic droit et "
                         "un seul raccourci, retire-la : « Montrer le désinstalleur », "
                         "puis double-clique « unins000 ».",
                         kind="warn",
                         buttons=[("Plus tard", None),
                                  ("Montrer le désinstalleur",
                                   lambda: reveal_path(uninstaller))],
                         auto_ms=30000)
        else:
            self.message("Deux Cerclic installés",
                         "La version de Cerclic installée sans le Microsoft Store est "
                         "encore là. Pour n'avoir qu'un « Cerclic », désinstalle-la dans "
                         "Applications installées : c'est le Cerclic qui n'a pas "
                         "« Options avancées » dans son menu.",
                         kind="warn",
                         buttons=[("Plus tard", None),
                                  ("Ouvrir les applications", package.open_apps_settings)],
                         auto_ms=30000)

    def _apply_mac(self) -> None:
        """The Finder's Quick Action and opening at login, rewritten at each start
        so that they point to where Cerclic.app is now."""
        from .mac import integration as mac
        if mac.app_bundle() is None:                   # running from the sources
            return
        try:
            if self.settings.get("context_menu"):
                mac.install_quick_action()
            else:
                mac.remove_quick_action()
        except Exception:
            log_exception("action rapide du Finder")
        try:
            mac.set_autostart(bool(self.settings.get("autostart")))
        except Exception:
            log_exception("ouverture à la connexion")

    def uninstall_mac(self) -> None:
        """Take Cerclic out of macOS, then quit (Cerclic.app goes to the Trash next)."""
        try:
            from .mac.integration import cleanup
            cleanup()
            log("Cerclic retiré du Finder et de l'ouverture de session")
        except Exception:
            log_exception("désinstallation")
        self.quit()

    def hotkey_combo(self) -> tuple[int, int]:
        return int(self.settings.get("hotkey_mods")), int(self.settings.get("hotkey_vk"))

    def hotkey_label(self) -> str:
        return hotkeys().label(*self.hotkey_combo())

    def _apply_hotkey(self, restart: bool = False) -> None:
        """Register the shortcut as set (again if `restart`), or remove it."""
        want = (bool(self.settings.get("hotkey")) and hotkey_supported()
                and not self._hotkey_paused
                and not os.environ.get("CERCLIC_NO_INTEGRATION"))
        mods, vk = self.hotkey_combo()
        if self.hotkey is not None and (not want or restart
                                        or (self.hotkey.mods, self.hotkey.vk) != (mods, vk)):
            self.hotkey.stop()
            self.hotkey = None
            self.hotkey_ok = None
        if want and self.hotkey is None:
            Hotkey = hotkeys().Hotkey
            self._hk_serial += 1
            serial = self._hk_serial
            # each answer carries its registration's number: a late answer
            # about a replaced combination is ignored
            self.hotkey = Hotkey(on_hotkey=self.bridge.hotkey.emit,
                                 on_status=lambda ok: self.bridge.hotkey_status.emit(serial, ok),
                                 mods=mods, vk=vk)
            self.hotkey.start()

    def _pause_hotkey(self, paused: bool) -> None:
        """While a new shortcut is being recorded, the current one is released
        (otherwise Windows would swallow it before the settings window sees it)."""
        self._hotkey_paused = paused
        self._apply_hotkey()

    def _on_hotkey_status(self, serial: int, ok: bool) -> None:
        if self.hotkey is None or serial != self._hk_serial:
            return                      # an older registration, already replaced
        self.hotkey_ok = ok
        combo = (self.hotkey.mods, self.hotkey.vk)
        trying, self._trying = self._trying, None
        win = self._settings_window()
        if ok:
            self._good_combo = combo
        elif trying is not None and trying != combo:
            # The combination just chosen is taken: keep the one that worked.
            label = hotkeys().label
            refused, kept = label(*combo), label(*trying)
            self.settings.set("hotkey_mods", trying[0])
            self.settings.set("hotkey_vk", trying[1])
            self.settings.save()
            if win is not None:
                self._hotkey_note = (f"{refused} est déjà utilisé par {OS_NAME} ou une "
                                     f"autre application. Ton raccourci reste {kept}.")
                win.show_combo(*trying)
            else:
                self.message(f"Raccourci {refused} indisponible",
                             f"{OS_NAME} ou une autre application l'utilise déjà. "
                             f"Ton raccourci reste {kept}.", kind="warn")
            self._apply_hotkey(restart=True)
            return
        if win is not None:
            note, self._hotkey_note = self._hotkey_note, ""
            win.set_hotkey_status(ok, note)
        elif not ok:
            fallback = (" ; le clic droit « Cerclic » marche toujours"
                        if self.settings.get("context_menu") else "")
            self.message(f"Raccourci {self.hotkey_label()} indisponible",
                         f"{OS_NAME} ou une autre application l'utilise déjà. Choisis-en "
                         f"un autre dans Cerclic{fallback}.",
                         kind="warn", buttons=[("Plus tard", None),
                                               ("Changer de raccourci", self._open_hotkey_page)])

    def right_click_how(self) -> str:
        """How to reach the right-click entry on this system."""
        if IS_MAC:
            return "clic droit, Actions rapides, puis « Cerclic »"
        if os.name == "nt" and not self.packaged:
            try:
                from .win import shell
                if shell.is_windows_11() and not shell.classic_menu_enabled():
                    return "clic droit, « Afficher d'autres options », puis « Cerclic »"
            except Exception:
                pass
        return "clic droit, puis « Cerclic »"

    # -- requests ------------------------------------------------------------------------
    def handle_request(self, cmd: str, paths: list) -> None:
        log(f"demande : {cmd} ({len(paths)} fichier(s))")
        try:
            if cmd == "open":
                self.open_wheel(paths, source="menu")
            elif cmd in ("hello", "settings"):
                self.open_settings()
            elif cmd == "quit":
                self.quit()
        except Exception:
            log_exception(f"demande {cmd} a échoué")
            self.message("Cerclic a rencontré un problème",
                         f"Les détails sont dans {log_path()}", kind="error")

    def _on_hotkey(self) -> None:
        # One read at a time; a read stuck on a frozen Explorer window does not
        # block the shortcut for more than a few seconds (its late answer is dropped).
        if self._reading_selection and time.monotonic() - self._reading_since < 4:
            return
        self._reads += 1
        n = self._reads
        self._reading_selection = n
        self._reading_since = time.monotonic()

        def read():
            try:
                if IS_MAC:
                    from .mac.selection import NotAllowed, finder_selection
                    try:
                        paths = finder_selection()
                    except NotAllowed:
                        self.bridge.finder_refused.emit(n)
                        return
                else:
                    from .win.selection import foreground_selection
                    paths = foreground_selection()
            except Exception:
                log_exception("lecture de la sélection")
                paths = []
            self.bridge.selection.emit(n, paths)

        threading.Thread(target=read, daemon=True, name="cerclic-selection").start()

    def _on_selection(self, n: int, paths: list) -> None:
        if n != self._reading_selection:
            return
        self._reading_selection = 0
        self.open_wheel(paths, source="hotkey")

    def _on_finder_refused(self, n: int) -> None:
        if n != self._reading_selection:
            return
        self._reading_selection = 0
        from .mac.integration import open_automation_settings
        self.message("Autorise Cerclic à lire ta sélection",
                     "Réglages Système, Confidentialité et sécurité, Automatisation : "
                     "coche « Finder » sous Cerclic. Le clic droit, Actions rapides, "
                     "« Cerclic » marche sans cela.", kind="warn",
                     buttons=[("Plus tard", None),
                              ("Ouvrir les réglages", open_automation_settings)],
                     auto_ms=25000)

    # -- files sent by macOS ---------------------------------------------------------------
    def _file_opened(self, path: str) -> None:
        self.files_received = True
        self._opened.append(path)
        self._opened_timer.start()          # one request for the whole bunch

    def _open_received(self) -> None:
        paths, self._opened = self._opened, []
        if paths:
            self.handle_request("open", paths)

    # -- wheel ---------------------------------------------------------------------------
    def open_wheel(self, paths: list, source: str = "menu") -> None:
        asked = list(paths)
        paths = clean_selection(paths)
        if self.session is not None and source == "menu" and self.session.can_merge():
            self.session.add([p for p in paths if kind_of(p) != "other"])
            return
        supported = [p for p in paths if kind_of(p) != "other"]
        if not supported:
            if asked and not paths:
                self.message("Fichier inaccessible",
                             "Ce fichier n'est pas dans un dossier normal (archive ZIP, "
                             "téléphone…). Copie-le dans un dossier, puis réessaie.")
            elif paths:
                self.message("Aucune action pour ce type de fichier",
                             "Cerclic travaille sur les images, les PDF, les vidéos "
                             "et les sons.")
            else:
                self.message("Sélectionne d'abord un fichier",
                             "Clique sur une image, un PDF, une vidéo ou un son dans "
                             f"{FILES_APP} ou sur le Bureau, puis appuie sur "
                             f"{self.hotkey_label()}."
                             + (f" Ou : {self.right_click_how()}."
                                if self.settings.get("context_menu") else ""))
            return
        if self.session is not None:
            self.session.close()
        self.session = WheelSession(self, supported, QCursor.pos(), source)

    # -- action flow -------------------------------------------------------------------------
    def start_action(self, action_id: str, paths: list[str], choice_opts: dict,
                     pos: QPoint) -> None:
        action = registry.get(action_id)
        files = registry.files_for(action, paths)
        if not files:
            return
        opts = {"quality": int(self.settings.get("compress_quality")),
                "jpg_quality": int(self.settings.get("jpg_quality"))}
        if self.settings.get("output_mode") == "folder" and self.settings.get("output_folder"):
            opts["_out_dir"] = self.settings.get("output_folder")
        opts.update(choice_opts)
        log(f"action {action_id} sur {len(files)} fichier(s)")
        if action.ui == "clipboard":
            self._copy_image(files[0])
            self.focus_back_later()
            return
        self._drive(self._flow(action, files, opts, pos))

    def _copy_image(self, path: str) -> None:
        """Put the picture on the clipboard (decoded in the background)."""
        from .actions import images
        from .ui.editor_base import Loader, qimage_from_pil
        if getattr(self, "_clip_loader", None) is None:
            self._clip_loader = Loader(self)
            self._clip_loader.done.connect(self._copied)
        self._clip_loader.run(lambda: qimage_from_pil(images.clipboard_image(path)))

    def _copied(self, img, err) -> None:
        if err or img is None or img.isNull():
            self.message("Copie impossible", err or "Image illisible.", kind="error")
            return
        QApplication.clipboard().setImage(img)
        log("image copiée dans le presse-papiers")
        self.message("Image copiée", f"Colle-la où tu veux avec {MOD_KEY} + V.", kind="ok",
                     auto_ms=3500)

    def _drive(self, gen, value=None) -> None:
        """Run a flow: each `yield ask` shows a window and resumes with its answer."""
        try:
            ask = gen.send(value)
        except StopIteration:
            self.focus_back_later()
            return
        except Exception:
            log_exception("déroulé d'une action")
            self.message("Cerclic a rencontré un problème",
                         f"Les détails sont dans {log_path()}", kind="error")
            self.focus_back_later()
            return
        ask(lambda result: self._drive(gen, result))

    def focus_back_later(self) -> None:
        """macOS: once the wheel and its popups are gone, the Finder (where the
        files are) gets the keyboard back, as Windows does by itself."""
        if IS_MAC:
            QTimer.singleShot(250, self._focus_back)

    def _focus_back(self) -> None:
        if QApplication.applicationState() != Qt.ApplicationActive:
            return                              # the user already went elsewhere
        if self.session is not None:
            return
        for w in list(self._live):
            try:
                if isinstance(w, QWidget) and w.isVisible():
                    return                      # an editor or a question is open
            except RuntimeError:
                pass
        win = self._settings_window()
        if win is not None and win.isVisible():
            return                              # the user is in Cerclic's window
        from .mac.foreground import give_back_to_finder
        give_back_to_finder()

    def _flow(self, action, files, opts, pos):
        from .actions import pdf as pdf_actions
        if action.id in registry.PASSWORD_AWARE:
            # Each protected PDF is asked for by name (a password already typed
            # for another one is tried first: often they share it).
            ok_label = "Déverrouiller" if action.id == "pdf_unlock" else "Continuer"
            passwords: dict[str, str] = {}
            for f in [f for f in files if pdf_actions.needs_password(f)]:
                pw = next((k for k in dict.fromkeys(passwords.values())
                           if pdf_actions.password_ok(f, k)), None)
                hint = f"« {os.path.basename(f)} » est protégé."
                tries = 0
                while pw is None:
                    if tries == 4:
                        self.message("Mot de passe incorrect", "Rien n'a été créé.",
                                     kind="error")
                        return
                    typed = yield self._ask_text("Mot de passe du PDF", hint, pos,
                                                 password=True, ok_label=ok_label)
                    if typed is None:
                        return
                    tries += 1
                    if pdf_actions.password_ok(f, typed):
                        pw = typed
                    else:
                        hint = (f"Mot de passe incorrect pour « {os.path.basename(f)} ». "
                                "Réessaie.")
                passwords[f] = pw
            if passwords:
                opts["passwords"] = passwords
        first_pw = registry._pw(opts, files[0])
        for need in action.needs:
            if need in ("crop", "social", "compress") and len(files) == 1 \
                    and kind_of(files[0]) == "image":
                from .actions.images import page_count
                pages = page_count(files[0])
                if pages > 1:                  # a scan: say so before any popup
                    first = {"crop": "Rogner n'en garderait que la première",
                             "social": "Seule la première serait mise au format",
                             "compress": "Compresser n'en garderait que la première"}[need]
                    self.message(f"« {os.path.basename(files[0])} » a {pages} pages",
                                 f"{first}. Utilise « En PDF » pour les garder toutes"
                                 + (f", puis {action.label} sur le PDF."
                                    if need in ("crop", "compress") else "."))
                    return
            if need == "crop":
                from .ui.crop_editor import CropEditor
                res = yield self._ask_editor(
                    lambda: CropEditor(files[0], first_pw), pos)
                if res is None:
                    return
                opts.update(res)
            elif need == "place_sig":
                sig = self.settings.get("signature")
                if not sig or not os.path.exists(sig):
                    from .ui.signature import SignaturePad
                    res = yield self._ask_editor(SignaturePad, pos)
                    if res is None:
                        return
                    sig = res["signature"]
                    self.settings.set("signature", sig)
                    self.settings.save()
                from .ui.signature import SignPlacer
                res = yield self._ask_editor(
                    lambda: SignPlacer(files[0], sig, first_pw), pos)
                if res is None:
                    return
                if res["signature"] != self.settings.get("signature"):
                    self.settings.set("signature", res["signature"])
                    self.settings.save()
                opts.update(res)
            elif need == "pages":
                from .ui.pages_editor import PagesEditor
                res = yield self._ask_editor(
                    lambda: PagesEditor(files[0], first_pw), pos)
                if res is None:
                    return
                opts.update(res)
            elif need == "trim":
                from .ui.trim_editor import TrimEditor
                res = yield self._ask_editor(lambda: TrimEditor(files[0]), pos)
                if res is None:
                    return
                opts.update(res)
            elif need == "compress":
                from .ui.compress_editor import CompressEditor
                kind = action.category
                levels = dict(self.settings.get("compress_levels") or {})
                res = yield self._ask_editor(lambda: CompressEditor(
                    files, kind, quality=int(self.settings.get("compress_quality")),
                    level=levels.get(kind), opts=opts), pos)
                if res is None:
                    return
                if "quality" in res:                       # proposed next time
                    self.settings.set("compress_quality", int(res["quality"]))
                if "level" in res:
                    levels[kind] = res["level"]
                    self.settings.set("compress_levels", levels)
                self.settings.save()
                opts.update(res)
            elif need == "social":
                from .ui.social_editor import SocialEditor
                kind = "video" if action.category == "video" else "image"
                last = dict(self.settings.get("social_last") or {})
                was = last.get(kind) if isinstance(last.get(kind), list) else []
                res = yield self._ask_editor(
                    lambda: SocialEditor(files, *(was + [None, None])[:2]), pos)
                if res is None:
                    return
                last[kind] = [res["social"], res["social_mode"]]   # proposed next time
                self.settings.set("social_last", last)
                self.settings.save()
                opts.update(res)
            elif need == "text":
                txt = yield self._ask_text("Texte du filigrane",
                                           "Il sera écrit en diagonale sur chaque page.",
                                           pos, default="CONFIDENTIEL")
                if txt is None:
                    return
                opts["text"] = txt
            elif need == "new_password":
                pw = yield self._ask_text("Mot de passe à mettre",
                                          "Il sera demandé pour ouvrir le PDF. "
                                          "L'original reste sans mot de passe.",
                                          pos, password=True, ok_label="Protéger")
                if pw is None:
                    return
                opts["new_password"] = pw
        if self.settings.get("output_mode") == "ask":
            folder = yield self._ask_folder(files[0], pos)
            if not folder:
                _drop_precomputed(opts)
                return                      # cancelled: nothing is created
            opts["_out_dir"] = folder
        self._run_job(action, files, opts, pos, attempts=0)

    def _ask_folder(self, src: str, pos=None):
        """« Me demander à chaque fois »: where the result goes, the original's
        folder proposed first, in front. The wheel has just closed: on Windows
        the question hangs on a tiny invisible window brought to the front
        first (else it could stay behind the Explorer); on macOS, Cerclic
        itself comes forward."""
        def ask(cb):
            def run():
                from PySide6.QtWidgets import QFileDialog
                anchor = None
                if IS_WINDOWS:
                    anchor = QWidget(None, Qt.Tool | Qt.FramelessWindowHint
                                     | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)
                    anchor.setAttribute(Qt.WA_TranslucentBackground)
                    anchor.setGeometry(QRect(pos if pos is not None else QCursor.pos(),
                                             QSize(1, 1)))
                    anchor.show()
                    bring_to_front(int(anchor.winId()))
                    self._live.add(anchor)
                else:
                    bring_to_front(0)
                try:
                    folder = QFileDialog.getExistingDirectory(
                        anchor, "Où enregistrer le résultat ?", os.path.dirname(src))
                finally:
                    if anchor is not None:
                        self._live.discard(anchor)
                        anchor.close()
                        anchor.deleteLater()
                cb(os.path.normpath(folder) if folder else None)
            QTimer.singleShot(0, run)
        return ask

    def _ask_text(self, title, subtitle, pos, password=False, default="",
                  ok_label="OK"):
        def ask(cb):
            from .ui.bubble import PromptBubble
            bubble = PromptBubble(title, subtitle, password=password, default=default,
                                  ok_label=ok_label)
            state = {"done": False}

            def finish(value):
                if state["done"]:
                    return
                state["done"] = True
                self._live.discard(bubble)
                cb(value)

            bubble.accepted.connect(finish)
            bubble.cancelled.connect(lambda: finish(None))
            self._live.add(bubble)
            bubble.popup_at(pos)
        return ask

    def _ask_editor(self, factory, pos=None):
        def ask(cb):
            editor = factory()
            state = {"done": False}

            def finish(value):
                if state["done"]:
                    return
                state["done"] = True
                self._live.discard(editor)
                cb(value)

            editor.accepted.connect(finish)
            editor.cancelled.connect(lambda: finish(None))
            self._live.add(editor)
            editor.start(pos if pos is not None else QCursor.pos())
        return ask

    # -- jobs -----------------------------------------------------------------------------------
    def _run_job(self, action, files, opts, pos, attempts: int) -> None:
        from .ui.cards import JobCard
        job = Job(action.id, files, dict(opts), journal=self.journal)
        card = JobCard(action.card_title)
        state = {"shown": False}

        def show_card():
            if not state["shown"] and not job.finished:
                state["shown"] = True
                self.cards.add(card)

        def on_done(result):
            job.finished = True
            self._live.discard(job)
            if not result.ok:
                _drop_precomputed(opts)      # not taken by the action: it goes
            QTimer.singleShot(0, _gc_now)
            log(f"résultat {result.action_id} : "
                + (f"ok, {len(result.outputs)} fichier(s) en {result.seconds:.1f} s"
                   if result.ok else f"{'annulé' if result.cancelled else 'échec'} : "
                                     f"{result.error}"))
            if result.needs_password and attempts < 3:
                if state["shown"]:
                    card.close()
                else:
                    card.deleteLater()
                self._drive(self._retry_password(action, files, opts, pos, attempts,
                                                 result.error, result.password_path))
                return
            card.finish(result, note=_elsewhere_note(files, result.outputs,
                                                     opts.get("_out_dir")))
            if not state["shown"]:
                state["shown"] = True
                self.cards.add(card)
            else:
                self.cards.relayout()

        job.progress.connect(card.set_progress)
        job.done.connect(on_done)
        card.cancel_requested.connect(job.cancel_event.set)
        self._live.add(job)
        job.start()
        QTimer.singleShot(250, show_card)

    def _retry_password(self, action, files, opts, pos, attempts, error, path=""):
        pw = yield self._ask_text("Mot de passe du PDF", error, pos, password=True,
                                  ok_label="Réessayer")
        if pw is None:
            return
        opts = dict(opts)
        if path:                               # that file's password, the others kept
            passwords = dict(opts.get("passwords") or {})
            passwords[path] = pw
            opts["passwords"] = passwords
        else:
            opts.pop("passwords", None)
            opts["password"] = pw
        self._run_job(action, files, opts, pos, attempts + 1)

    # -- messages, help, settings ------------------------------------------------------------------
    def message(self, title: str, text: str = "", kind: str = "info",
                buttons=None, auto_ms: int = 8000) -> None:
        from .ui.cards import MessageCard
        self.cards.add(MessageCard(title, text, kind, buttons, auto_ms))

    def enable_classic_menu(self) -> None:
        from .win import shell
        try:
            shell.set_classic_menu(True)
            self.settings.set("classic_menu", True)
            self.settings.set("classic_menu_by_cerclic", True)
            self.settings.save()
        except Exception:
            log_exception("menu classique")
            return
        self.message("Menu complet activé",
                     "Il s'applique au redémarrage de l'Explorateur. Les fenêtres de "
                     "dossiers ouvertes vont se fermer.",
                     buttons=[("Plus tard", None),
                              ("Redémarrer l'Explorateur", self._restart_explorer)],
                     auto_ms=20000)

    def disable_classic_menu(self) -> None:
        from .win import shell
        try:
            shell.set_classic_menu(False)
        except Exception:
            log_exception("menu classique")
        self.settings.set("classic_menu", False)
        self.settings.set("classic_menu_by_cerclic", False)
        self.settings.save()
        self.message("Menu de Windows 11 rétabli",
                     "Il s'applique au redémarrage de l'Explorateur.",
                     buttons=[("Plus tard", None),
                              ("Redémarrer l'Explorateur", self._restart_explorer)],
                     auto_ms=20000)

    def _restart_explorer(self) -> None:
        from .win import shell
        try:
            shell.restart_explorer()
        except Exception:
            log_exception("redémarrage de l'Explorateur")

    # -- Cerclic's window (settings) -------------------------------------------------------
    def _settings_window(self):
        if self._settings_win is None:
            return None
        try:
            self._settings_win.isVisible()
            return self._settings_win
        except RuntimeError:
            self._settings_win = None
            return None

    def open_settings(self, welcome: bool = False) -> None:
        win = self._settings_window()
        if win is not None:
            if win.isMinimized():
                win.showNormal()
            win.show()
            win.raise_()
            win.activateWindow()
            return
        from .ui.settings_window import SettingsWindow
        win11 = classic = False
        if os.name == "nt" and not self.packaged:   # (the Store version's entry is
            from .win import shell                    # in Windows 11's short menu)
            win11 = shell.is_windows_11()
            classic = win11 and shell.classic_menu_enabled()
        win = SettingsWindow(self.settings, windows_11=win11, welcome=welcome,
                             classic_enabled=classic, store=self.packaged)
        win.changed.connect(lambda key: self._setting_changed(win, key))
        win.capturing.connect(self._pause_hotkey)
        win.draw_signature.connect(lambda: self._draw_signature(win))
        win.quit_requested.connect(self.quit)
        win.uninstall_requested.connect(self.uninstall_mac)
        win.destroyed.connect(lambda *_: setattr(self, "_settings_win", None))
        self._settings_win = win
        win.set_hotkey_status(self.hotkey_ok if self.hotkey is not None else None)
        win.show_centered(QCursor.pos())

    def _open_hotkey_page(self) -> None:
        self.open_settings()
        win = self._settings_window()
        if win is not None:
            win.show_page("hotkey")

    def _setting_changed(self, win, key: str) -> None:
        if key in ("context_menu", "autostart"):
            self._apply_shell(changed=key)
        elif key == "hotkey":
            self._apply_hotkey()
            try:
                win.set_hotkey_status(self.hotkey_ok if self.hotkey is not None else None)
            except RuntimeError:
                pass
        elif key == "hotkey_combo":
            self._hotkey_paused = False
            self._trying = self._good_combo     # kept if the new one is taken
            self._apply_hotkey(restart=True)
        elif key == "classic_menu" and os.name == "nt":
            from .win import shell
            choice = win.classic_choice()
            if choice is not None and choice != shell.classic_menu_enabled():
                if choice:
                    self.enable_classic_menu()
                else:
                    self.disable_classic_menu()

    def _draw_signature(self, win) -> None:
        def flow():
            from .ui.signature import SignaturePad
            try:
                anchor = win.geometry().center()
            except RuntimeError:
                anchor = QCursor.pos()
            res = yield self._ask_editor(SignaturePad, anchor)
            if res:
                self.settings.set("signature", res["signature"])
                self.settings.save()
                try:
                    win.refresh_signature()
                except RuntimeError:
                    pass
        self._drive(flow())

    def quit(self) -> None:
        self.shutdown()
        self.qapp.quit()

    def shutdown(self) -> None:
        """Stop cleanly: also when macOS quits Cerclic itself (Cmd + Q, logout)."""
        if getattr(self, "_stopped", False):
            return
        self._stopped = True
        log("arrêt de Cerclic")
        if self.hotkey is not None:
            self.hotkey.stop()
        win = self._settings_window()
        if win is not None:
            win.close()
        if self.session is not None:
            self.session.close()
        running = [j for j in self._live if isinstance(j, Job)]
        for job in running:
            job.cancel_event.set()
        # Let stopped actions clean up what they started (a few seconds at most).
        deadline = time.monotonic() + 6
        while any(not j.finished for j in running) and time.monotonic() < deadline:
            self.qapp.processEvents(QEventLoop.AllEvents, 50)
            time.sleep(0.02)
        self.cards.close_all()
        self.tray.hide()


# ----- startup ---------------------------------------------------------------------------------

def _qt_messages(mode, context, message) -> None:
    if "QWindowsWindow::setGeometry" in message or "propagateSizeHints" in message:
        return
    log(f"Qt: {message}")


def _install_crash_logging() -> None:
    def hook(exc_type, exc, tb):
        import traceback
        log("erreur non gérée :\n" + "".join(traceback.format_exception(exc_type, exc, tb)))

    def thread_hook(args):
        hook(args.exc_type, args.exc_value, args.exc_traceback)

    sys.excepthook = hook
    threading.excepthook = thread_hook


def _collect_on_gui_thread(qapp) -> QTimer:
    """Python's cycle collector may run in whatever thread happens to allocate,
    and destroying a Qt window outside the interface thread crashes. So
    automatic collection is off, and the interface thread collects regularly
    (reference counting still frees almost everything at once)."""
    import gc
    gc.disable()
    timer = QTimer(qapp, interval=20_000)
    timer.timeout.connect(lambda: gc.collect())
    timer.start()
    return timer


def run_resident(cmd: str, paths: list[str], lock) -> int:
    """Start the resident Cerclic, then perform the request that started it."""
    _install_crash_logging()
    if getattr(sys, "frozen", False):
        # Started by a right-click, Cerclic would otherwise keep the clicked
        # file's folder as its working folder for the whole session: that USB
        # key could not be ejected, that folder not renamed or deleted.
        from .sysenv import neutral_dir
        try:
            os.chdir(neutral_dir())
        except OSError:
            pass
    qInstallMessageHandler(_qt_messages)
    qapp = QApplication.instance() or FileOpenApp(sys.argv[:1])
    qapp.setQuitOnLastWindowClosed(False)
    qapp.setApplicationName(APP_NAME)
    qapp.setApplicationVersion(__version__)
    from .ui.theme import apply_app_theme
    apply_app_theme(qapp)
    qapp._cerclic_gc = _collect_on_gui_thread(qapp)
    log(f"démarrage de Cerclic {__version__} (journal : {log_path()})")
    if not QSystemTrayIcon.isSystemTrayAvailable():
        log("zone de notification indisponible au démarrage, nouvel essai")
    try:
        app = CerclicApp(qapp)
    except Exception:
        log_exception("échec au démarrage")
        return 1
    app._lock = lock  # held for the life of the process
    qapp.aboutToQuit.connect(app.shutdown)

    def first_request():
        first = not app.settings.get("welcome_shown")
        if cmd == "open":
            app.open_wheel(paths, source="menu")
        elif app.files_received:
            pass                         # macOS started Cerclic to open files: the wheel
        elif cmd in ("hello", "settings") or first:
            if first:
                app.settings.set("welcome_shown", True)
                app.settings.save()
            app.open_settings(welcome=first)

    # macOS hands the files it started Cerclic for a moment after the start:
    # the settings only open if none came.
    QTimer.singleShot(700 if IS_MAC and cmd == "hello" else 0, first_request)
    return qapp.exec()
