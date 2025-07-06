@echo off
cd /d "%~dp0\.."

echo ====================================
echo Personal Finance CLI Application
echo ====================================
echo.

echo [1/3] Cleaning previous build...
call .\gradlew.bat clean
if %ERRORLEVEL% neq 0 (
    echo ERROR: Clean failed!
    pause
    exit /b 1
)

echo.
echo [2/3] Building application...
call .\gradlew.bat build
if %ERRORLEVEL% neq 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo [3/3] Starting Personal Finance Application...
echo.
call .\gradlew.bat run --console=plain -q

echo.
echo Application finished.
pause
