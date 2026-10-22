"""Hand-off between launches and the resident Cerclic (pipe protocol)."""
import os

import pytest

from cerclic import launcher


def test_parse_args():
    assert launcher.parse_args([]) == ("hello", [])
    assert launcher.parse_args(["--background"]) == ("background", [])
    assert launcher.parse_args(["--open", "a.jpg", "b.pdf"]) == ("open", ["a.jpg", "b.pdf"])
    assert launcher.parse_args(["C:\\x\\photo.jpg"]) == ("open", ["C:\\x\\photo.jpg"])
    assert launcher.parse_args(["--quit"]) == ("quit", [])
    assert launcher.parse_args(["--cleanup"]) == ("cleanup", [])
    assert launcher.parse_args(["--settings"]) == ("settings", [])
    assert launcher.parse_args(["--weird", "--open", "x"]) == ("open", ["x"])


def test_encode_decode_roundtrip():
    paths = ["C:\\Users\\Saïd El Araifa\\Images\\été 2026 (1).jpg", "D:\\doc.pdf"]
    data = launcher.encode("open", paths)
    assert launcher.decode(data) == ("open", paths)
    assert launcher.decode(b"garbage") is None
    assert launcher.decode(b"CERCLIC/1\nrm -rf\nEND\n") is None      # unknown command
    assert launcher.decode(launcher.encode("open", ["bad\npath"])) == ("open", [])


def test_send_without_resident_is_false():
    assert launcher.send("hello", [], timeout=0.5) is False


def test_send_reaches_request_server(qtbot):
    from cerclic.app import RequestServer
    server = RequestServer(launcher.server_name())
    assert server.ok
    got = []
    server.request.connect(lambda c, p: got.append((c, p)))

    import threading
    result = {}

    def client():
        result["ok"] = launcher.send("open", ["/tmp/a.jpg", "/tmp/b.pdf"], timeout=3)

    t = threading.Thread(target=client)
    t.start()
    qtbot.waitUntil(lambda: bool(got), timeout=3000)
    t.join(3)
    assert result.get("ok") is True
    assert got == [("open", ["/tmp/a.jpg", "/tmp/b.pdf"])]
    server.server.close()


def test_resident_lock_is_exclusive():
    if os.name == "nt":
        pytest.skip("Windows mutex covered by the Windows build tests")
    first = launcher.ResidentLock()
    second = launcher.ResidentLock()
    assert first.already is False and second.already is True


def test_installer_registry_is_up_to_date():
    """installer/registry.iss must list every supported extension, exactly as
    the app registers them (regenerate with scripts/gen_installer_registry.py)."""
    import importlib.util
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    spec = importlib.util.spec_from_file_location(
        "gen", os.path.join(root, "scripts", "gen_installer_registry.py"))
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    with open(os.path.join(root, "installer", "registry.iss"), encoding="utf-8",
              newline="") as f:
        assert f.read() == gen.render()
