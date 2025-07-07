@echo off
REM SBI Transaction Extractor - Windows Batch Script
REM This script runs the SBI transaction extractor with organized output

echo.
echo ===============================================
echo    SBI Transaction Extractor - Easy Run
echo ===============================================
echo.

REM Get the script directory
set SCRIPT_DIR=%~dp0

REM Set the Python executable path
set PYTHON_EXE="%SCRIPT_DIR%.venv\Scripts\python.exe"

REM Check if Python environment exists
if not exist %PYTHON_EXE% (
    echo ERROR: Python environment not found!
    echo Please make sure the .venv directory exists in %SCRIPT_DIR%
    echo.
    pause
    exit /b 1
)

REM Check if statements folder exists
if exist "%SCRIPT_DIR%statements\" (
    echo Found statements folder with PDF files
) else (
    echo WARNING: 'statements' folder not found
    echo Will search for PDF files in current directory
)

REM Run the extractor
echo Running SBI Transaction Extractor...
echo.

%PYTHON_EXE% "%SCRIPT_DIR%sbi_extractor.py" %*

echo.
echo ===============================================
echo Process completed. Check the output folder.
echo ===============================================
echo.
pause
