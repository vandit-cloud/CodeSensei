@echo off
REM CodeSensei Desktop App - Quick Start Script (Windows)

echo.
echo ========================================
echo    CodeSensei Desktop App Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [OK] Python found
echo.

echo Installing dependencies...
pip install -r requirements_desktop.txt

echo.
echo ========================================
echo    Starting CodeSensei Desktop App
echo ========================================
echo.

python desktop_app_fixed.py

pause
