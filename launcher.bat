@echo off
echo ====================================
echo   Personal Finance CLI Launcher
echo ====================================
echo.
echo Choose an option:
echo.
echo   1. Run Application (Full Clean Build)
echo   2. Quick Run (Incremental Build)
echo   3. Run Tests
echo   4. Build Distribution
echo   5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    call scripts\run-app.bat
) else if "%choice%"=="2" (
    call scripts\quick-run.bat
) else if "%choice%"=="3" (
    call scripts\run-tests.bat
) else if "%choice%"=="4" (
    call scripts\build-dist.bat
) else if "%choice%"=="5" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice. Please select 1-5.
    pause
    goto :eof
)
