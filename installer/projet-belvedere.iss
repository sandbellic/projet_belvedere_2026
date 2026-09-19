#ifndef MyAppVersion
#define MyAppVersion "0.0.0"
#endif

[Setup]
AppName=Projet Hotel Belvedere
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\ProjetBelvedere
DefaultGroupName=Projet Belvedere

OutputDir=..\dist
OutputBaseFilename=ProjetBelvedere-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "..\dist\projet-belvedere.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Projet Belvedere"; Filename: "{app}\projet-belvedere.exe"
Name: "{autodesktop}\Projet Belvedere"; Filename: "{app}\projet-belvedere.exe"

[Run]
Filename: "{app}\projet-belvedere.exe"; Description: "Lancer Hotel Belvedere"; Flags: nowait postinstall skipifsilent