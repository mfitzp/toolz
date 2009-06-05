; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{83324364-3699-409A-A64C-E29C8FC4C898}
AppName=Bruker2mzXML
AppVerName=Bruker2mzXML 0.9
AppPublisher=Death Star Inc.
DefaultDirName={pf}\Bruker2mzXML
DefaultGroupName=Bruker2mzXML
OutputBaseFilename=Bruker2mzXML_Setup
SetupIconFile=C:\SVN\icons\Clone.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Documents and Settings\d3p483\workspace\Bruker2mzXML\dist\Bruker2mzXML.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Documents and Settings\d3p483\workspace\Bruker2mzXML\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\Bruker2mzXML"; Filename: "{app}\Bruker2mzXML.exe"
Name: "{group}\{cm:UninstallProgram,Bruker2mzXML}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Bruker2mzXML"; Filename: "{app}\Bruker2mzXML.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Bruker2mzXML.exe"; Description: "{cm:LaunchProgram,Bruker2mzXML}"; Flags: nowait postinstall skipifsilent

