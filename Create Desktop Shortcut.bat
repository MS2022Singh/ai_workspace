@echo off
cd /d "%~dp0"
echo Creating desktop shortcut...

powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell; " ^
  "$desktop = $ws.SpecialFolders('Desktop'); " ^
  "$shortcut = $ws.CreateShortcut(\"$desktop\AI Workspace.lnk\"); " ^
  "$shortcut.TargetPath = '%~dp0venv\Scripts\pythonw.exe'; " ^
  "$shortcut.Arguments = '\"%~dp0main.py\"'; " ^
  "$shortcut.WorkingDirectory = '%~dp0'; " ^
  "$shortcut.IconLocation = '%~dp0assets\icon.ico'; " ^
  "$shortcut.Description = 'Open AI Workspace'; " ^
  "$shortcut.Save()"

if exist "%USERPROFILE%\Desktop\AI Workspace.lnk" (
    echo Done. "AI Workspace" shortcut added to your Desktop.
    echo It launches Python directly now, with no script file involved --
    echo no more security warning when opening it.
) else (
    echo Something went wrong creating the shortcut.
)
pause
