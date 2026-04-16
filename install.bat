@echo off
REM install.bat - Windows installation script for SerialCLI
REM This script installs SerialCLI globally on Windows systems
REM Usage: run as Administrator

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo SerialCLI - Windows Installation Script
echo ============================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator
    echo Please right-click on this script and select "Run as administrator"
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

echo Detected Python installation:
python --version

REM Install pip requirements
echo.
echo Installing required packages...
pip install --upgrade pip setuptools wheel pyserial
if %errorLevel% neq 0 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

REM Install SerialCLI in development mode
echo.
echo Installing SerialCLI...
pip install -e .
if %errorLevel% neq 0 (
    echo ERROR: Failed to install SerialCLI
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✓ Installation completed successfully!
echo ============================================================
echo.
echo You can now run SerialCLI from any command prompt:
echo   SerialCLI
echo.
pause
