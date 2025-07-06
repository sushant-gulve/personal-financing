@echo off
cd /d "%~dp0\.."

echo ====================================
echo Personal Finance CLI - Build Distribution
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
echo [2/3] Running tests...
call .\gradlew.bat test
if %ERRORLEVEL% neq 0 (
    echo ERROR: Tests failed!
    pause
    exit /b 1
)

echo.
echo [3/3] Building distribution packages...
call .\gradlew.bat build distTar distZip
if %ERRORLEVEL% neq 0 (
    echo ERROR: Distribution build failed!
    pause
    exit /b 1
)

echo.
echo ✅ Build completed successfully!
echo.
echo 📦 Distribution packages created:
echo   - build\distributions\personal financing-1.0.0.tar
echo   - build\distributions\personal financing-1.0.0.zip
echo   - build\libs\personal financing-1.0.0.jar
echo.
echo 🚀 To run the application:
echo   java -jar "build\libs\personal financing-1.0.0.jar"
echo.
pause
