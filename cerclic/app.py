"""Cerclic application: tray icon, global gesture, radial menu, action runner.

Flow: the mouse hook detects the gesture and fires `Bridge.fire` (a queued
signal, so the handler runs on the GUI thread); the handler reads the current
selection, shows the radial menu, gathers any extra input the chosen action
needs, then runs it in a worker thread and shows a result toast.
"""
from __future__ import annotations

import os
import sys

from PySide6.QtCore import QObject, Signal, Qt, QThread
from PySide6.QtWidgets import (QApplication, QSystemTrayIcon, QMenu,
                               QFileDialog, QMessageBox)

from . import APP_NAME, __version__, engine
from .settings import Settings
from .actions import registry
from .ui.radial import RadialMenu
from .ui.crop import CropDialog
from .ui.toast import Toast
from .ui.dialogs import ask_password, ask_text, Busy
from .ui.settings_window import SettingsWindow
from .ui.trayicon import make_icon
from .log import log, log_path


def _summary(paths: list[str]) -> str:
    if len(paths) == 1:
        name = os.path.basename(paths[0])
        return name if len(name) <= 22 else name[:19] + "..."
    return f"{len(paths)} fichiers"


class Bridge(QObject):
    fire = Signal(int, int)
    status = Signal(bool, str)


class Worker(QThread):
    done = Signal(object)

    def __init__(self, action_id, paths, opts):
        super().__init__()
        self._args = (action_id, paths, opts)

    def run(self):
        self.done.emit(engine.run(*self._args))


class CerclicApp(QObject):
    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self.settings = Settings.load()
        self._refs = []            # keep transient windows alive
        self._radial = None
        self._busy = None
        self._worker = None
        self._active = False       # a gesture is being handled

        self.bridge = Bridge()
        self.bridge.fire.connect(self._on_gesture, Qt.QueuedConnection)
        self.bridge.status.connect(self._on_hook_status, Qt.QueuedConnection)

        self._build_tray()
        self._start_hook()
        self._apply_autostart()

    # -- tray ----------------------------------------------------------------
    def _build_tray(self):
        self.tray = QSystemTrayIcon(make_icon(), self.app)
        self.tray.setToolTip(f"{APP_NAME} {__version__}")
        menu = QMenu()
        menu.addAction("Paramètres", self.open_settings)
        menu.addAction("À propos", self._about)
        menu.addSeparator()
        menu.addAction("Quitter", self.quit)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._tray_activated)
        self.tray.show()
        self._menu = menu
        hint = {"left_hold": "Maintiens le clic gauche sur un fichier",
                "right_hold": "Maintiens le clic droit sur un fichier",
                "double_right": "Double clic droit sur un fichier"}.get(
                    self.settings.get("gesture"), "Sélectionne un fichier")
        hint += ", ou appuie sur Ctrl+Alt+Espace."
        self.tray.showMessage("Cerclic est prêt", hint,
                              QSystemTrayIcon.Information, 4000)

    def _tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.open_settings()

    def _about(self):
        box = QMessageBox()
        box.setWindowTitle("À propos de Cerclic")
        box.setText(
            f"<b>{APP_NAME}</b> {__version__}<br><br>"
            "Maintiens le clic gauche sur un fichier pour ouvrir le menu d'actions (geste réglable).<br>"
            "Images, PDF et vidéos, sans ouvrir d'application.")
        box.exec()

    # -- hook ----------------------------------------------------------------
    def _start_hook(self):
        from .win.mouse_hook import GestureHook
        self.hook = GestureHook(
            on_trigger=lambda x, y: self.bridge.fire.emit(x, y),
            mode=self.settings.get("gesture"),
            double_ms=int(self.settings.get("double_ms")),
            hold_ms=int(self.settings.get("hold_ms")),
            on_status=lambda ok, detail: self.bridge.status.emit(ok, detail))
        self.hook.start()

    def _on_hook_status(self, ok: bool, detail: str):
        if not ok:
            self.tray.showMessage(
                "Cerclic : geste souris indisponible",
                f"{detail}. Le raccourci Ctrl+Alt+Espace reste utilisable.",
                QSystemTrayIcon.Warning, 8000)

    def _restart_hook(self):
        try:
            self.hook.stop()
        except Exception:
            pass
        self._start_hook()

    def _apply_autostart(self):
        try:
            from .win.autostart import set_autostart
            set_autostart(bool(self.settings.get("autostart")))
        except Exception:
            pass

    # -- gesture handling ----------------------------------------------------
    def _on_gesture(self, x: int, y: int):
        if self._active:
            log("geste ignoré : une roue est déjà ouverte")
            return
        paths = self._current_selection()
        log(f"sélection lue : {len(paths)} fichier(s) "
            + ", ".join(os.path.basename(p) for p in paths[:5]))
        if not paths:
            log("aucune sélection lue, ouverture du sélecteur de fichiers")
            paths = self._pick_files()
        if not paths:
            return
        menu = registry.menu_for(paths)
        if not menu:
            log("aucune action pour ces fichiers")
            self._toast_info("Aucune action pour ce type de fichier")
            return
        log("roue ouverte : " + ", ".join(menu.keys()))
        self._active = True
        self._selection = paths
        self._radial = RadialMenu(menu, _summary(paths),
                                  theme=self.settings.get("ring_theme"),
                                  primary_only=bool(self.settings.get("primary_only")))
        self._radial.selected.connect(self._on_action)
        self._radial.cancelled.connect(self._on_cancel)
        self._radial.popup_at(x, y)

    def _current_selection(self):
        try:
            from .win.selection import selected_paths
            return selected_paths()
        except Exception as exc:
            log(f"erreur de lecture de la sélection : {exc!r}")
            return []

    def _pick_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            None, "Cerclic, choisir un ou plusieurs fichiers")
        return files

    def _on_cancel(self):
        self._active = False
        self._radial = None

    def _on_action(self, action_id: str):
        self._radial = None
        paths = registry.paths_for_action(action_id, self._selection)
        log(f"action {action_id} sur {len(paths)} fichier(s)")
        opts = self._base_opts()
        try:
            if not self._gather_needs(action_id, paths, opts):
                self._active = False
                return
        except Exception as exc:
            self._active = False
            self._toast_info(f"Annulé : {exc}")
            return
        self._busy = Busy(f"{registry.get(action_id).label}...")
        self._busy.show()
        self._worker = Worker(action_id, paths, opts)
        self._worker.done.connect(self._on_done)
        self._worker.start()

    def _base_opts(self) -> dict:
        return {
            "quality": int(self.settings.get("compress_quality")),
            "max_side": int(self.settings.get("resize_max_side")),
            "signature": self.settings.get("signature"),
            "degrees": 90,
        }

    def _gather_needs(self, action_id, paths, opts) -> bool:
        """Fill opts for any required input. Return False if the user cancels."""
        for key in engine.missing_inputs(action_id, opts):
            if key == "crop_box":
                box = CropDialog.get_box(paths[0])
                if not box:
                    return False
                opts["crop_box"] = box
            elif key == "signature":
                sig = self.settings.get("signature")
                if not sig or not os.path.exists(sig):
                    QMessageBox.information(
                        None, "Cerclic",
                        "Ajoute d'abord ta signature dans les paramètres.")
                    self.open_settings()
                    return False
                opts["signature"] = sig
            elif key == "password":
                pw = ask_password("Mot de passe du PDF :")
                if not pw:
                    return False
                opts["password"] = pw
            elif key == "text":
                txt = ask_text("Texte du filigrane :", "CONFIDENTIEL")
                if not txt:
                    return False
                opts["text"] = txt
        # unlock: optional password, ask once if the file looks encrypted
        if action_id == "pdf_unlock":
            pw = ask_password("Mot de passe (laisser vide si aucun) :")
            opts["password"] = pw or ""
        return True

    def _on_done(self, result):
        if self._busy:
            self._busy.close()
            self._busy = None
        self._active = False
        log(f"résultat {result.action_id} : "
            + (f"ok, {len(result.outputs)} fichier(s)" if result.ok
               else f"échec, {result.error}"))
        label = registry.get(result.action_id).label
        toast = Toast(label if result.ok else f"{label} a échoué",
                      result.outputs, ok=result.ok, error=result.error)
        toast.show()
        self._refs = [w for w in self._refs if w.isVisible()]
        self._refs.append(toast)

    def _toast_info(self, text: str):
        toast = Toast(text, [], ok=False, error="")
        toast.show()
        self._refs.append(toast)

    # -- settings ------------------------------------------------------------
    def open_settings(self):
        win = SettingsWindow(self.settings, on_apply=self._settings_applied)
        win.exec()

    def _settings_applied(self):
        self._apply_autostart()
        self._restart_hook()

    def quit(self):
        try:
            self.hook.stop()
        except Exception:
            pass
        self.tray.hide()
        self.app.quit()


def _log_crash(exc: BaseException) -> str:
    import traceback
    from .settings import config_dir
    path = os.path.join(config_dir(), "cerclic.log")
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n--- crash ---\n")
            traceback.print_exc(file=f)
    except Exception:
        pass
    return path


def main():
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName(APP_NAME)
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Cerclic",
                             "Barre des tâches indisponible.")
        return 1
    # Single instance: if Cerclic already runs, say so and stop.
    from PySide6.QtNetwork import QLocalServer, QLocalSocket
    probe = QLocalSocket()
    probe.connectToServer("cerclic-instance")
    if probe.waitForConnected(300):
        QMessageBox.information(None, "Cerclic",
                                "Cerclic est déjà lancé (icône près de l'horloge).")
        return 0
    server = QLocalServer()
    QLocalServer.removeServer("cerclic-instance")
    server.listen("cerclic-instance")
    log(f"démarrage de Cerclic {__version__} (journal : {log_path()})")
    try:
        cerclic = CerclicApp(app)
        _ = cerclic
        return app.exec()
    except Exception as exc:
        path = _log_crash(exc)
        QMessageBox.critical(None, "Cerclic, erreur au démarrage",
                             f"{exc}\n\nDétails écrits dans :\n{path}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
