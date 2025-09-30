@echo off
echo SavePassword Uninstaller
echo =======================
echo.

set /p CONFIRM="Are you sure you want to uninstall SavePassword? (y/N): "
if /i "%CONFIRM%" neq "y" (
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo.
set /p BACKUP="Do you want to create a backup of your password database? (Y/n): "
if /i "%BACKUP%" equ "n" (
    echo Skipping backup...
) else (
    echo Creating backup...
    if exist "data" (
        if not exist "backup" mkdir "backup"
        xcopy "data" "backup\data_%date:/=-%_%time::=-%" /E /I /H /Y
        echo Backup created in 'backup' folder.
    ) else (
        echo No data folder found to backup.
    )
)

echo.
echo Removing application files...

:: Remove desktop shortcut
if exist "%PUBLIC%\Desktop\SavePassword.lnk" (
    del "%PUBLIC%\Desktop\SavePassword.lnk"
    echo Removed desktop shortcut.
)

:: Remove start menu folder
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\SavePassword" (
    rmdir /S /Q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\SavePassword"
    echo Removed start menu entries.
)

:: Remove settings file
if exist "settings.json" (
    del "settings.json"
    echo Removed settings file.
)

echo.
echo SavePassword has been uninstalled.
echo.
echo Note: Your password database in the 'data' folder has NOT been removed.
echo If you want to completely remove all data, manually delete the 'data' folder.
echo.

pause