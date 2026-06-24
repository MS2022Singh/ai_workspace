@echo off
cd /d "%~dp0"
if not exist venv (
    echo Please run run.bat first to set up the app, then run this again.
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
pip show pyinstaller >nul 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)
echo Building AI Workspace.exe ...
pyinstaller --noconfirm --noconsole --onedir --name "AI Workspace" ^
  --icon "assets\icon.ico" ^
  --add-data "frontend;frontend" ^
  main.py

echo.
echo Done. Find it in: dist\AI Workspace\AI Workspace.exe
echo You can right-click that .exe and "Send to > Desktop (create shortcut)"
echo for a fully standalone app icon (no Python window, ever).
pause
