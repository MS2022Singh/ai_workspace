@echo off
cd /d "%~dp0"
if not exist venv (
    echo Please run run.bat first to set up the app.
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
echo Installing optional media tools (adds MP4 slideshow export)...
pip install opencv-python-headless numpy
echo.
echo Done. MP4 export is now available in Media Tools (GIF always worked
echo without this -- this just adds the MP4 option).
pause
