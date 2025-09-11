@echo off
echo PSTimer Windows Build Script
echo =============================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo Error: main.py not found. Please run this script from the PSTimer directory.
    pause
    exit /b 1
)

REM Install PyInstaller if not available
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Run the build script
echo Running build script...
python build_dist.py

echo.
echo Build complete! Check the generated files.
pause
