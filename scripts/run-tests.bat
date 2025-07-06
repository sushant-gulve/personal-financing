@echo off
cd /d "%~dp0\.."

echo ====================================
echo Personal Finance CLI - Run Tests
echo ====================================
echo.

echo [1/2] Building and running tests...
call .\gradlew.bat test
if %ERRORLEVEL% neq 0 (
    echo ERROR: Tests failed!
    pause
    exit /b 1
)

echo.
echo [2/2] Generating test report...
echo Test report available at: build\reports\tests\test\index.html

echo.
echo All tests completed successfully!
pause
