@echo off
echo ====================================
echo Personal Finance CLI - Quick Run
echo ====================================
echo.

echo [1/2] Building application (incremental)...
call .\gradlew.bat build
if %ERRORLEVEL% neq 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo [2/2] Starting Personal Finance Application...
echo.
call .\gradlew.bat run --console=plain -q

echo.
echo Application finished.
pause
