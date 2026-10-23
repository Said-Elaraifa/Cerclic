; Inno Setup script for Cerclic: per-user install, no admin rights needed.
; Built by scripts/build_windows.sh (Linux + Wine) or the GitHub workflow.
; The version is passed with /DMyAppVersion=x.y.z.

#ifndef MyAppVersion
  #define MyAppVersion "0.4.0"
#endif

#define MyAppName "Cerclic"
#define MyAppPublisher "Said El Araifa"
#define MyAppExeName "Cerclic.exe"

[Setup]
AppId={{B7E9B9B1-5C2A-4E2E-9E8A-CERCLIC00001}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
VersionInfoVersion={#MyAppVersion}
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
; An update keeps the user's choices (start with Windows, right-click entry off).
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "Cerclic"; ValueData: """{app}\{#MyAppExeName}"" --background"; Flags: uninsdeletevalue; Check: SettingOn('autostart')
#include "registry.iss"

[UninstallDelete]
; settings, handwritten signature, journal
Type: filesandordirs; Name: "{userappdata}\Cerclic"

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
  { older versions, or a copy that did not answer (this account only) }
  if Exec(ExpandConstant('{sys}\taskkill.exe'),
          '/F /FI "USERNAME eq ' + GetUserNameString() + '" /IM {#MyAppExeName} /IM CerclicOpen.exe',
          '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0) then
    Sleep(1500);   { a stopped program releases its files a moment later }
end;

{ An update keeps what the user turned off in Cerclic (settings.json is
  written by Cerclic with "key": true/false). }
function SettingOn(Key: String): Boolean;
var
  Json: AnsiString;
begin
  Result := True;
  if LoadStringFromFile(ExpandConstant('{userappdata}\Cerclic\settings.json'), Json) then
    Result := Pos('"' + Key + '": false', Json) = 0;
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
var
  ResultCode: Integer;
begin
  if CurUninstallStep = usUninstall then
  begin
    StopCerclic();
    { what Cerclic itself added to Windows (right-click entry, start with
      Windows, full Windows 11 menu if it turned it on) }
    Exec(ExpandConstant('{app}\{#MyAppExeName}'), '--cleanup', '', SW_HIDE,
         ewWaitUntilTerminated, ResultCode);
    RemoveClassicMenuIfOurs();
  end;
end;
