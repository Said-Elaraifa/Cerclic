; Inno Setup script for Cerclic: per-user install, no admin rights needed.
; Built by scripts/build_windows.sh (Linux + Wine) or the GitHub workflow.
; The version is passed with /DMyAppVersion=x.y.z.

#ifndef MyAppVersion
  #define MyAppVersion "0.2.0"
#endif

#define MyAppName "Cerclic"
#define MyAppPublisher "Said El Araifa"
#define MyAppExeName "Cerclic.exe"

[Setup]
AppId={{B7E9B9B1-5C2A-4E2E-9E8A-CERCLIC00001}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\{#MyAppName}
DisableDirPage=yes
DisableProgramGroupPage=yes
DisableReadyPage=yes
PrivilegesRequired=lowest
OutputDir=..\dist_installer
OutputBaseFilename=CerclicSetup-{#MyAppVersion}
SetupIconFile=..\assets\cerclic.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0.17763
CloseApplications=no
RestartApplications=no
ChangesAssociations=yes

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "Créer un raccourci sur le Bureau"; GroupDescription: "Raccourcis :"

[Files]
Source: "..\dist\Cerclic\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[InstallDelete]
; files of older versions that are not shipped any more
Type: files; Name: "{app}\Lancer Cerclic.bat"

[Icons]
Name: "{userprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{userdesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "Cerclic"; ValueData: """{app}\{#MyAppExeName}"" --background"; Flags: uninsdeletevalue
#include "registry.iss"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Lancer Cerclic"; Flags: nowait postinstall skipifsilent

[Code]
const
  QuitWindowTitle = 'Cerclic.Quit';
  WM_CLOSE = $0010;
  ClassicMenuKey = 'Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}';

{ Stop a running Cerclic before files are replaced or removed. Cerclic 0.2+
  keeps an invisible window: closing it makes Cerclic stop cleanly (running
  actions are cancelled and cleaned up). No program is started, nothing can
  hang: the wait is bounded, then anything left is ended. }
procedure StopCerclic();
var
  Wnd: HWND;
  Tries, ResultCode: Integer;
begin
  Wnd := FindWindowByWindowName(QuitWindowTitle);
  if Wnd <> 0 then
  begin
    PostMessage(Wnd, WM_CLOSE, 0, 0);
    Tries := 0;
    while (FindWindowByWindowName(QuitWindowTitle) <> 0) and (Tries < 80) do
    begin
      Sleep(100);
      Tries := Tries + 1;
    end;
  end;
  { older versions, or a copy that did not answer }
  Exec(ExpandConstant('{sys}\taskkill.exe'), '/F /IM {#MyAppExeName}', '', SW_HIDE,
       ewWaitUntilTerminated, ResultCode);
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  StopCerclic();
  Result := '';
end;

{ Undo the Windows 11 full right-click menu only if Cerclic turned it on. }
procedure RemoveClassicMenuIfOurs();
var
  Json: AnsiString;
begin
  if LoadStringFromFile(ExpandConstant('{userappdata}\Cerclic\settings.json'), Json) then
    if Pos('"classic_menu_by_cerclic": true', Json) > 0 then
      RegDeleteKeyIncludingSubkeys(HKEY_CURRENT_USER, ClassicMenuKey);
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then
  begin
    StopCerclic();
    RemoveClassicMenuIfOurs();
  end;
end;
