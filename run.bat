@echo off
cd /d "%~dp0"
if not exist venv (
    echo Creating virtual environment...
    py -3 -m venv venv
)
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul
echo Checking dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Dependency install failed. See errors above.
    echo If you're on a brand-new Python version ^(3.13+^), try installing
    echo Python 3.12 from python.org instead, delete the "venv" folder
    echo in this directory, and run this script again.
    pause
    exit /b 1
)
echo.
echo Launching AI Workspace...
timeout /t 1 >nul
start "" "%~dp0venv\Scripts\pythonw.exe" "%~dp0main.py"
exit
