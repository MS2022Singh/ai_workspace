@echo off
:: Self-elevate to Administrator if not already running as one.
>nul 2>&1 net session
if %errorlevel% neq 0 (
    echo Requesting administrator permission...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

echo Adding a Windows Firewall rule to allow AI Workspace's port
echo through on Private networks (e.g. your home WiFi)...
echo.

netsh advfirewall firewall delete rule name="AI Workspace (Mobile Access)" >nul 2>&1
netsh advfirewall firewall add rule name="AI Workspace (Mobile Access)" dir=in action=allow protocol=TCP localport=8765-8785 profile=private

if %errorlevel% equ 0 (
    echo.
    echo Done. Ports 8765-8785 are now allowed through Windows Firewall
    echo on Private networks. Restart AI Workspace, then try your phone again.
) else (
    echo.
    echo Something went wrong adding the firewall rule. If this PC is
    echo managed by a workplace/IT department, a separate security
    echo product may be blocking this instead of Windows Firewall, and
    echo you may need to ask IT for help.
)
pause
