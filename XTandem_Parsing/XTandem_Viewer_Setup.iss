; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{F2BDA5BA-E177-4A6B-936F-CE42DADC0288}
AppName=X!Tandem Data Viewer
AppVerName=X!Tandem Viewer 0.8
AppPublisher=Death Star Inc.
AppPublisherURL=www.google.com
AppSupportURL=www.google.com
AppUpdatesURL=www.google.com
DefaultDirName={pf}\X!Tandem Data Viewer
DefaultGroupName=X!Tandem Data Viewer
AllowNoIcons=yes
OutputBaseFilename=XT_Viewer_Setup
SetupIconFile=C:\Documents and Settings\d3p483\My Documents\Python\GCAlign\icons\Clone.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Documents and Settings\d3p483\My Documents\Python\XTandem_Parsing\dist\XT_Viewer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Documents and Settings\d3p483\My Documents\Python\XTandem_Parsing\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\X!Tandem Data Viewer"; Filename: "{app}\XT_Viewer.exe"
Name: "{group}\{cm:UninstallProgram,X!Tandem Data Viewer}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\X!Tandem Data Viewer"; Filename: "{app}\XT_Viewer.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\XT_Viewer.exe"; Description: "{cm:LaunchProgram,X!Tandem Data Viewer}"; Flags: nowait postinstall skipifsilent

