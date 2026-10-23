"""Build Cerclic's Microsoft Store package from the Windows build.

    scripts/build_windows.sh        (makes dist/Cerclic and dist_native/)
    python scripts/store/build.py   (needs PySide6 and lxml: the dev environment)

Writes in dist_store/:
  Cerclic-<v>.msix          for Partner Center, with the identity Partner Center
                            gave (store/identity.json); Microsoft signs it
  Cerclic-<v>-test.zip      to try the package first on a Windows 11 PC: the
                            same package under a test identity (unsigned), with
                            scripts that install and remove it
Every package is checked after it is written: manifest against Microsoft's
schemas, ZIP and block map read back, logos resolved through resources.pri.
"""
from __future__ import annotations

import json
import os
import shutil
import struct
import sys
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import assets    # noqa: E402
import manifest  # noqa: E402
import msix      # noqa: E402
import pri       # noqa: E402

APP = os.path.join(ROOT, "dist", "Cerclic")
MENU_DLL = os.path.join(ROOT, "dist_native", "CerclicMenu.dll")
OUT = os.path.join(ROOT, "dist_store")
IDENTITY = os.path.join(ROOT, "store", "identity.json")
KIT = os.path.join(ROOT, "store", "test-kit")
# Left out of the package: the classic version's own helpers, data of a run.
SKIP_TOP = {"Données Cerclic", "CerclicOpen.exe", "cerclic.log"}


def load_identities() -> dict:
    with open(IDENTITY, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {k: v for k, v in data.items() if not k.startswith("_")}


def make_layout(folder: str, identity: dict, display_name: str) -> bytes:
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)
    for name in os.listdir(APP):
        if name in SKIP_TOP or name.lower().startswith("unins"):
            continue
        src = os.path.join(APP, name)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(folder, name))
        else:
            shutil.copy2(src, os.path.join(folder, name))
    shutil.copy2(MENU_DLL, os.path.join(folder, "CerclicMenu.dll"))
    assets.write_assets(folder)
    assets.write_index(folder, identity["Name"])
    xml = manifest.build_manifest(identity, display_name=display_name)
    with open(os.path.join(folder, msix.MANIFEST), "wb") as f:
        f.write(xml)
    return xml


def pe_hardening(path: str) -> list[str]:
    """Binaries without ASLR or DEP (reported, the Store does not require them
    for desktop apps, but they should be there)."""
    weak = []
    for root, _, names in os.walk(path):
        for n in names:
            if not n.lower().endswith((".exe", ".dll", ".pyd")):
                continue
            p = os.path.join(root, n)
            try:
                with open(p, "rb") as f:
                    head = f.read(4096)
                pe = struct.unpack_from("<I", head, 0x3C)[0]
                if head[pe:pe + 4] != b"PE\0\0":
                    continue
                opt = pe + 24
                flags = struct.unpack_from("<H", head, opt + 70)[0]
                if not (flags & 0x40 and flags & 0x100):
                    weak.append(os.path.relpath(p, path))
            except (OSError, struct.error):
                continue
    return weak


def check_package(path: str, identity: dict, layout: str) -> None:
    """Everything Windows and Partner Center will look at, read back from the file."""
    report = msix.verify(path)
    xml = report["manifest"]
    errors = manifest.validate(xml)
    if errors and not (len(errors) == 1 and "lxml absent" in errors[0]):
        raise SystemExit("AppxManifest.xml refusé par le schéma :\n  " + "\n  ".join(errors))
    names = {n.replace("\\", "/") for n in report["names"]}
    for need in ("Cerclic.exe", "CerclicMenu.dll", "resources.pri", "LICENCES.txt"):
        if need not in names:
            raise SystemExit(f"{need} manque dans le paquet")
    index = pri.read_pri(msix.read_file(path, "resources.pri"))
    if index["checksum"] != index["computed_checksum"] or index["name"] != identity["Name"]:
        raise SystemExit("resources.pri incohérent")
    from PySide6.QtGui import QImage
    for logical, cands in index["resources"].items():
        for quals, value in cands:
            rel = value.replace("\\", "/")
            if rel not in names:
                raise SystemExit(f"logo absent : {rel}")
            img = QImage(os.path.join(layout, rel))
            q = dict(quals)
            base = os.path.basename(logical)
            want = None
            if "TargetSize" in q:
                want = (int(q["TargetSize"]),) * 2
            elif q.get("Scale") == "200":
                sizes = {"Square44x44Logo.png": (44, 44), "Square150x150Logo.png": (150, 150),
                         "Wide310x150Logo.png": (310, 150), "SmallTile.png": (71, 71),
                         "LargeTile.png": (310, 310), "StoreLogo.png": (50, 50)}
                w, h = sizes[base]
                want = (w * 2, h * 2)
            if want and (img.width(), img.height()) != want:
                raise SystemExit(f"{rel} : {img.width()}x{img.height()} au lieu de {want}")
    for logo in ("Square44x44Logo.png", "Square150x150Logo.png", "Wide310x150Logo.png",
                 "SmallTile.png", "LargeTile.png", "StoreLogo.png"):
        if f"Files/Assets/{logo}" not in index["resources"]:
            raise SystemExit(f"logo sans entrée dans resources.pri : {logo}")
    print(f"   vérifié : {report['files']} fichiers, {report['bytes'] / 1e6:.0f} Mo, "
          f"manifeste conforme, logos trouvés")


def short(version: str) -> str:
    """'0.7.0.0' -> '0.7.0', for file names."""
    return version[:-2] if version.endswith(".0") and version.count(".") == 3 else version


def build(kind: str, identity: dict, version: str) -> str:
    test = kind == "test"
    v = short(version)
    name = f"Cerclic-{v}-test.msix" if test else f"Cerclic-{v}.msix"
    layout = os.path.join(OUT, f"layout-{kind}")
    print(f"== paquet {kind} ({identity['Name']})")
    make_layout(layout, identity, "Cerclic (test)" if test else "Cerclic")
    out = os.path.join(OUT, name)
    count = msix.pack(layout, out)
    print(f"   {count} fichiers, {os.path.getsize(out) / 1e6:.0f} Mo : {out}")
    check_package(out, identity, layout)
    return out


def test_kit(package: str, version: str) -> str:
    out = os.path.join(OUT, f"Cerclic-{short(version)}-test.zip")
    folder = f"Cerclic-{short(version)}-test"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_STORED) as z:
        z.write(package, f"{folder}/{os.path.basename(package)}")
        for n in sorted(os.listdir(KIT)):
            z.write(os.path.join(KIT, n), f"{folder}/{n}")
    print(f"== kit de test : {out}")
    return out


def listing_kit(version: str) -> str:
    """Everything for the submission: the guide, the texts to paste, the
    screenshots and the tile icon (drawn by screenshots.py in its own process:
    it needs its own screen settings)."""
    import subprocess
    done = subprocess.run([sys.executable, os.path.join(HERE, "screenshots.py")],
                          capture_output=True, text=True)
    if done.returncode != 0:
        raise SystemExit("captures d'écran impossibles :\n" + done.stdout + done.stderr)
    fiche = os.path.join(OUT, "fiche")
    texts = os.path.join(ROOT, "store", "publication")
    out = os.path.join(OUT, f"Cerclic-{short(version)}-publication-Store.zip")
    folder = f"Cerclic-{short(version)}-publication-Store"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n in sorted(os.listdir(texts)):
            z.write(os.path.join(texts, n), f"{folder}/{n}")
        z.write(os.path.join(fiche, "icone-300x300.png"), f"{folder}/icone-300x300.png")
        for n in sorted(os.listdir(os.path.join(fiche, "captures"))):
            z.write(os.path.join(fiche, "captures", n), f"{folder}/captures/{n}")
    print(f"== kit de publication : {out}")
    return out


def main() -> int:
    if not os.path.exists(os.path.join(APP, "Cerclic.exe")):
        raise SystemExit("dist/Cerclic manque : lance d'abord scripts/build_windows.sh")
    if not os.path.exists(MENU_DLL):
        raise SystemExit("CerclicMenu.dll manque : lance native/build.sh")
    os.makedirs(OUT, exist_ok=True)
    version = manifest.app_version()
    ids = load_identities()
    weak = pe_hardening(APP)
    if weak:
        print("   sans ASLR ou DEP (à signaler, pas bloquant) : " + ", ".join(weak[:12]))
    start = time.time()
    test_pkg = build("test", ids["test"], version)
    test_kit(test_pkg, version)
    store = ids.get("store", {})
    if all(store.get(k) for k in ("Name", "Publisher", "PublisherDisplayName")):
        build("store", store, version)
    else:
        print("== paquet Store : en attente des trois valeurs de Partner Center "
              "(store/identity.json)")
    try:                    # (the packages never depend on the screenshots)
        listing_kit(version)
    except (SystemExit, OSError) as exc:
        print(f"== kit de publication non fait : {exc}")
    print(f"terminé en {time.time() - start:.0f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
