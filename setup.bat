@echo off
TITLE AI Workspace Core - Installer v3.0
echo Installing AI Workspace OS Kernel v3.0...
set INSTALL_DIR=%LOCALAPPDATA%\AI_Workspace_Core

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
xcopy /E /Y /I "%~dp0dist\AI_Workspace_Kernel" "%INSTALL_DIR%"

echo Creating Desktop Shortcut...
set SCRIPT="%TEMP%\CreateShortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\AI Workspace Core.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%INSTALL_DIR%\AI_Workspace_Kernel.exe" >> %SCRIPT%
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript //nologo %SCRIPT%
del %SCRIPT%

echo.
echo ===================================================
echo Installation complete! Launching AI Workspace OS...
echo ===================================================
start "" "%INSTALL_DIR%\AI_Workspace_Kernel.exe"
pause
