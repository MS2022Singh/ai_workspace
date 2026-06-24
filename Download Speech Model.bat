@echo off
cd /d "%~dp0"
if not exist venv (
    echo Please run run.bat first to set up the app.
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
python backend\download_speech_model.py
pause
