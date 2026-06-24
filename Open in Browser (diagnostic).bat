@echo off
cd /d "%~dp0"
if not exist venv (
    echo Please run run.bat first to set up the app.
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
echo Starting AI Workspace in browser mode...
echo This window will show live server logs. Leave it open while using the app.
echo Press Ctrl+C here to stop the server when you're done.
echo.
python main.py --browser
pause
