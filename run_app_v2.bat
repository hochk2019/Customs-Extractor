@echo off
chcp 65001 >nul
cls

echo.
echo ===============================================================================
echo           CUSTOMS EXTRACTOR V2 - CHAY UNG DUNG
echo ===============================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found!
    echo Please run install.bat first.
    pause
    exit /b 1
)

REM Run the V2 GUI application
cls
echo.
echo Starting Customs Extractor V2...
echo.

python customs_extractor_gui_v2.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Application encountered an error!
    pause
)

exit /b %ERRORLEVEL%
