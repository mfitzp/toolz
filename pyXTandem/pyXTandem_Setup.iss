; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{CE214061-11C7-4170-A0FC-F03D29EDCF8F}
AppName=pyXTandem
AppVerName=pyXTandem 0.8
AppPublisher=Death Start Inc.
AppPublisherURL=www.google.com
AppSupportURL=www.google.com
AppUpdatesURL=www.google.com
DefaultDirName={pf}\pyXTandem
DefaultGroupName=pyXTandem
AllowNoIcons=yes
OutputBaseFilename=pyXTandem_Setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Documents and Settings\d3p483\My Documents\Python\pyXTandem\dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Documents and Settings\d3p483\My Documents\Python\pyXTandem\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\pyXTandem"; Filename: "{app}\main.exe"
Name: "{group}\{cm:UninstallProgram,pyXTandem}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\pyXTandem"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,pyXTandem}"; Flags: nowait postinstall skipifsilent

