[Setup]
AppName=BookStore
AppVersion=1.0
DefaultDirName={pf}\BookStore
DefaultGroupName=BookStore
OutputDir=.
OutputBaseFilename=BookStore_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\BookStore.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "config\*"; DestDir: "{app}\config"; Flags: recursesubdirs
Source: "models\*"; DestDir: "{app}\models"; Flags: recursesubdirs
Source: "views\*"; DestDir: "{app}\views"; Flags: recursesubdirs
Source: "controllers\*"; DestDir: "{app}\controllers"; Flags: recursesubdirs
Source: "utils\*"; DestDir: "{app}\utils"; Flags: recursesubdirs

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Icons]
Name: "{group}\BookStore"; Filename: "{app}\BookStore.exe"
Name: "{commondesktop}\BookStore"; Filename: "{app}\BookStore.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\BookStore.exe"; Description: "Launch BookStore"; Flags: nowait postinstall skipifsilent
