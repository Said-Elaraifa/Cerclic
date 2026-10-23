"""AppxManifest.xml of the Microsoft Store package.

What it declares:
* Cerclic.exe, a full trust desktop app (runFullTrust), from Windows 10 2004;
* the right-click entry: CerclicMenu.dll (CLSID below), hosted by Windows in
  a COM surrogate, for every file type Cerclic works on;
* starting with Windows: a startup task launching Cerclic with --background;
* the logos (Assets, chosen through resources.pri).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import url2pathname
from xml.sax.saxutils import escape, quoteattr

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MENU_CLSID = "2E424C09-6978-44D7-88C6-0D6FBA9C0FD5"     # also in native/cerclic_menu.c
STARTUP_TASK = "CerclicStartup"                         # also in cerclic/win/package.py
APP_ID = "Cerclic"
MIN_VERSION = "10.0.19041.0"         # Windows 10 2004: uap10:Parameters (startup task)
MAX_TESTED = "10.0.26100.0"          # Windows 11 24H2
BACKGROUND = "#1C2B4B"               # behind the logos, where Windows puts a plate
DESCRIPTION = ("Rogner, signer, compresser, convertir tes images, PDF, vidéos et sons "
               "depuis le clic droit ou un raccourci.")
UNSIGNED_OID = "OID.2.25.311729368913984317654407730594956997722=1"

_NAME = re.compile(r"^[-.A-Za-z0-9]{3,50}$")


def app_version() -> str:
    """'0.7.0' -> '0.7.0.0' (the Store keeps the fourth number for itself)."""
    text = open(os.path.join(ROOT, "cerclic", "__init__.py"), encoding="utf-8").read()
    v = re.search(r'__version__ = "(\d+)\.(\d+)\.(\d+)"', text)
    if not v:
        raise ValueError("version de Cerclic introuvable")
    return ".".join(v.groups()) + ".0"


def file_types() -> list[str]:
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    from cerclic.paths import SUPPORTED_EXTS
    return sorted(SUPPORTED_EXTS)


def check_identity(identity: dict) -> None:
    for key in ("Name", "Publisher", "PublisherDisplayName"):
        if not identity.get(key):
            raise ValueError(f"identité incomplète : {key} manque")
    if not _NAME.match(identity["Name"]):
        raise ValueError(f"nom de paquet invalide : {identity['Name']!r}")
    if not identity["Publisher"].startswith("CN="):
        raise ValueError(f"éditeur invalide (doit commencer par CN=) : {identity['Publisher']!r}")


def build_manifest(identity: dict, version: str | None = None,
                   display_name: str = "Cerclic") -> bytes:
    check_identity(identity)
    version = version or app_version()
    verbs = "\n".join(
        f'            <desktop5:ItemType Type="{ext}">\n'
        f'              <desktop5:Verb Id="Cerclic" Clsid="{MENU_CLSID}"/>\n'
        f'            </desktop5:ItemType>'
        for ext in file_types())
    xml = f'''<?xml version="1.0" encoding="utf-8"?>
<Package
  xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
  xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
  xmlns:uap5="http://schemas.microsoft.com/appx/manifest/uap/windows10/5"
  xmlns:uap10="http://schemas.microsoft.com/appx/manifest/uap/windows10/10"
  xmlns:desktop4="http://schemas.microsoft.com/appx/manifest/desktop/windows10/4"
  xmlns:desktop5="http://schemas.microsoft.com/appx/manifest/desktop/windows10/5"
  xmlns:com="http://schemas.microsoft.com/appx/manifest/com/windows10"
  xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities"
  IgnorableNamespaces="uap uap5 uap10 desktop4 desktop5 com rescap">
  <Identity Name={quoteattr(identity["Name"])} Publisher={quoteattr(identity["Publisher"])}
            Version="{version}" ProcessorArchitecture="x64"/>
  <Properties>
    <DisplayName>{escape(display_name)}</DisplayName>
    <PublisherDisplayName>{escape(identity["PublisherDisplayName"])}</PublisherDisplayName>
    <Logo>Assets\\StoreLogo.png</Logo>
    <Description>{escape(DESCRIPTION)}</Description>
  </Properties>
  <Dependencies>
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="{MIN_VERSION}" MaxVersionTested="{MAX_TESTED}"/>
  </Dependencies>
  <Resources>
    <Resource Language="fr-FR"/>
  </Resources>
  <Capabilities>
    <rescap:Capability Name="runFullTrust"/>
  </Capabilities>
  <Applications>
    <Application Id="{APP_ID}" Executable="Cerclic.exe" EntryPoint="Windows.FullTrustApplication">
      <uap:VisualElements DisplayName={quoteattr(display_name)} Description={quoteattr(DESCRIPTION)}
          BackgroundColor="{BACKGROUND}"
          Square150x150Logo="Assets\\Square150x150Logo.png" Square44x44Logo="Assets\\Square44x44Logo.png">
        <uap:DefaultTile Wide310x150Logo="Assets\\Wide310x150Logo.png" Square310x310Logo="Assets\\LargeTile.png"
            Square71x71Logo="Assets\\SmallTile.png" ShortName="Cerclic">
          <uap:ShowNameOnTiles>
            <uap:ShowOn Tile="square150x150Logo"/>
            <uap:ShowOn Tile="wide310x150Logo"/>
            <uap:ShowOn Tile="square310x310Logo"/>
          </uap:ShowNameOnTiles>
        </uap:DefaultTile>
      </uap:VisualElements>
      <Extensions>
        <uap5:Extension Category="windows.startupTask" Executable="Cerclic.exe"
            EntryPoint="Windows.FullTrustApplication" uap10:Parameters="--background">
          <uap5:StartupTask TaskId="{STARTUP_TASK}" Enabled="true" DisplayName="Cerclic"/>
        </uap5:Extension>
        <desktop4:Extension Category="windows.fileExplorerContextMenus">
          <desktop4:FileExplorerContextMenus>
{verbs}
          </desktop4:FileExplorerContextMenus>
        </desktop4:Extension>
        <com:Extension Category="windows.comServer">
          <com:ComServer>
            <com:SurrogateServer DisplayName="Cerclic">
              <com:Class Id="{MENU_CLSID}" Path="CerclicMenu.dll" ThreadingModel="STA"/>
            </com:SurrogateServer>
          </com:ComServer>
        </com:Extension>
      </Extensions>
    </Application>
  </Applications>
</Package>
'''
    return xml.encode("utf-8")


# ----- checking against Microsoft's schemas (from the msix-packaging SDK) ---------------

SCHEMAS = os.path.join(ROOT, "store", "schemas")
_LOOSEN = [("[^\\x01-\\x1f]", "."), ("\\x01-\\x1f", ""), ("\\bms-resource:", "ms-resource:"),
           ("((?!\\%[Ii].*\\%[Ii]).)*", ".*")]


def validate(manifest: bytes) -> list[str]:
    """Errors found by Microsoft's AppxManifest schemas ([] when valid).
    Needs lxml (tests, build): returns ['lxml absent'] without it."""
    try:
        from lxml import etree
    except ImportError:
        return ["lxml absent : schéma non vérifié"]
    base = os.path.join(SCHEMAS, "Manifest", "Schema")
    files = {}
    for root, _, names in os.walk(base):
        for n in names:
            if n.endswith(".xsd"):
                path = os.path.join(root, n)
                with open(path, "rb") as f:
                    head = f.read(4000).decode("utf-8", "replace")
                ns = re.search(r'targetNamespace\s*=\s*"([^"]+)"', head)
                # (bundles are another kind of package; the server schema has a
                # typo libxml2 refuses, and nothing of it is used here)
                if ns and "Bundle" not in n and "ServerManifest" not in n:
                    files.setdefault(ns.group(1), path)
    # every namespace imported by its file, the foundation one last
    foundation = "http://schemas.microsoft.com/appx/manifest/foundation/windows10"
    # (file:// addresses: libxml2 ignores an import whose location has a
    # backslash, as every Windows path has)
    imports = "".join(
        f'<xs:import namespace="{ns}" schemaLocation="{escape(Path(path).as_uri())}"/>'
        for ns, path in sorted(files.items()) if ns != foundation)
    imports += (f'<xs:import namespace="{foundation}" '
                f'schemaLocation="{escape(Path(files[foundation]).as_uri())}"/>')
    master = ('<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" '
              'targetNamespace="urn:cerclic:all" elementFormDefault="qualified">'
              + imports + "</xs:schema>")

    class Patched(etree.Resolver):
        """A few of Microsoft's patterns use its own regex dialect (\\x01-\\x1f,
        \\b, look-ahead), unknown to XML Schema: they are loosened here (the
        values in Cerclic's manifest have nothing these would catch)."""

        def resolve(self, url, pubid, context):
            path = url2pathname(urlparse(url).path) if url.startswith("file:") else url
            if path.endswith(".xsd") and os.path.isfile(path):
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
                for old, new in _LOOSEN:
                    text = text.replace(old, new)
                return self.resolve_string(text, context, base_url=url)
            return None

    parser = etree.XMLParser()
    parser.resolvers.add(Patched())
    schema = etree.XMLSchema(etree.fromstring(master.encode("utf-8"), parser,
                                              base_url=Path(base).as_uri() + "/"))
    doc = etree.fromstring(manifest)
    if schema.validate(doc):
        return []
    return [f"ligne {e.line} : {e.message}" for e in schema.error_log]
