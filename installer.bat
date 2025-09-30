@echo off
echo SavePassword Installer
echo =====================
echo.

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This installer requires administrator privileges.
    echo Please run as Administrator.
    pause
    exit /b 1
)

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Installing Python...
    :: Download and install Python (simplified)
    echo Please install Python manually from python.org
    pause
    exit /b 1
)

echo Python is installed.
python --version

:: Install required packages
echo Installing required packages...
pip install -r requirements.txt

:: Create desktop shortcut
echo Creating shortcuts...
set SCRIPT_DIR=%~dp0
set SHORTCUT_PATH=%PUBLIC%\Desktop\SavePassword.lnk

:: Create start menu folder
set START_MENU_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\SavePassword

:: Create the application
echo Installation complete!
echo.
echo You can now run SavePassword using:
echo python main.py
echo.
echo Or use the portable version:
echo python portable_password_manager.py
echo.
pause