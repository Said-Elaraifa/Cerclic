; Inno Setup script for Cerclic: per-user install, no admin rights needed.
; Built by scripts/build_windows.sh (Linux + Wine) or the GitHub workflow.
; The version is passed with /DMyAppVersion=x.y.z.

#ifndef MyAppVersion
  #define MyAppVersion "0.7.0"
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
; the user chooses where Cerclic goes (an update proposes the current folder)
DisableDirPage=no
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

{ A folder as a PowerShell string: 'C:\...\' (a quote in it doubled). }
function PsFolder(Dir: String): String;
begin
  Dir := AddBackslash(Dir);
  StringChangeEx(Dir, '''', '''''', True);
  Result := '''' + Dir + '''';
end;

{ Stop a running Cerclic before files are replaced or removed. Cerclic 0.2+
  keeps an invisible window: closing it makes Cerclic stop cleanly (running
  actions are cancelled and cleaned up). No program is started, nothing can
  hang: the wait is bounded, then anything left is ended. OtherDir: the
  previous folder when an update moves Cerclic ('' otherwise). }
procedure StopCerclic(const OtherDir: String);
var
  Wnd: HWND;
  Tries, ResultCode: Integer;
  Dirs, Cmd: String;
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
  { older versions, or a copy that did not answer: only the programs of these
    folders (Cerclic from the Microsoft Store, installed elsewhere, keeps running) }
  Dirs := PsFolder(ExpandConstant('{app}'));
  if OtherDir <> '' then
    Dirs := Dirs + ', ' + PsFolder(OtherDir);
  Cmd := '$dirs = @(' + Dirs + '); $p = @(Get-Process -Name Cerclic,CerclicOpen -ErrorAction SilentlyContinue | ' +
         'Where-Object { $x = $_.Path; $x -and @($dirs | Where-Object { $x.StartsWith($_, [StringComparison]::OrdinalIgnoreCase) }).Count -gt 0 }); ' +
         'if ($p.Count -eq 0) { exit 1 }; $p | Stop-Process -Force; exit 0';
  if Exec(ExpandConstant('{sys}\WindowsPowerShell\v1.0\powershell.exe'),
          '-NoProfile -NonInteractive -ExecutionPolicy Bypass -Command "' + Cmd + '"',
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

{ Cerclic installs without administrator rights: a folder only an
  administrator may write to (Program Files...) cannot take it. Said on the
  folder page, before anything is copied. }
function DirWritable(const Dir: String): Boolean;
var
  Probe, Existing, D: String;
begin
  Result := False;
  { the nearest folder that already exists: the ones made for the test go again }
  Existing := RemoveBackslashUnlessRoot(Dir);
  while (not DirExists(Existing)) and (ExtractFileDir(Existing) <> Existing) do
    Existing := ExtractFileDir(Existing);
  if not ForceDirectories(Dir) then
    exit;
  Probe := AddBackslash(Dir) + 'cerclic-essai-ecriture.tmp';
  if SaveStringToFile(Probe, 'x', False) then
  begin
    DeleteFile(Probe);
    Result := True;
  end;
  D := RemoveBackslashUnlessRoot(Dir);
  while (Length(D) > Length(Existing)) and RemoveDir(D) do
    D := ExtractFileDir(D);
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  if (CurPageID = wpSelectDir) and not DirWritable(WizardDirValue()) then
  begin
    SuppressibleMsgBox('Cerclic ne peut pas s''installer dans ce dossier : Windows le protège ' +
           '(il faudrait des droits d''administrateur) ou il n''est pas accessible.' + #13#10 +
           'Choisis un dossier à toi, par exemple dans Documents, ou garde celui proposé.',
           mbError, MB_OK, IDOK);
    Result := False;
  end;
end;

{ An update installed into another folder than the previous one moves
  Cerclic: once the new copy is in place, Cerclic's own files go from the old
  folder (only those: anything else the user kept there stays), then the
  folder itself if nothing is left in it. The settings, in the user's
  profile, stay. A marker written in the new folder tells whether the old
  path is in fact the same folder (a mapped drive, a link...). }
var
  OldDir: String;

function SameDir(const A, B: String): Boolean;
begin
  Result := CompareText(RemoveBackslashUnlessRoot(A), RemoveBackslashUnlessRoot(B)) = 0;
end;

function Inside(const Child, Parent: String): Boolean;
begin
  Result := Pos(Lowercase(AddBackslash(Parent)), Lowercase(AddBackslash(Child))) = 1;
end;

procedure RemoveOldCopy(const Dir: String);
var
  D: String;
begin
  D := AddBackslash(Dir);
  DelTree(D + '_internal', True, True, True);
  DeleteFile(D + '{#MyAppExeName}');
  DeleteFile(D + 'CerclicOpen.exe');
  DeleteFile(D + 'LICENCES.txt');
  DeleteFile(D + 'Lancer Cerclic.bat');
  DelTree(D + 'unins*.*', False, True, False);
  RemoveDir(Dir);
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  NewDir, Marker: String;
begin
  if CurStep = ssInstall then
    OldDir := WizardForm.PrevAppDir;
  if CurStep = ssPostInstall then
  begin
    NewDir := ExpandConstant('{app}');
    if (OldDir <> '') and not SameDir(OldDir, NewDir) and not Inside(NewDir, OldDir)
       and FileExists(AddBackslash(OldDir) + '{#MyAppExeName}') then
    begin
      Marker := 'cerclic-nouveau-dossier.tmp';
      if SaveStringToFile(AddBackslash(NewDir) + Marker, 'x', False) then
      begin
        if not FileExists(AddBackslash(OldDir) + Marker) then
          RemoveOldCopy(OldDir);
        DeleteFile(AddBackslash(NewDir) + Marker);
      end;
    end;
  end;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  StopCerclic(WizardForm.PrevAppDir);
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
    StopCerclic('');
    { what Cerclic itself added to Windows (right-click entry, start with
      Windows, full Windows 11 menu if it turned it on) }
    Exec(ExpandConstant('{app}\{#MyAppExeName}'), '--cleanup', '', SW_HIDE,
         ewWaitUntilTerminated, ResultCode);
    RemoveClassicMenuIfOurs();
  end;
end;
