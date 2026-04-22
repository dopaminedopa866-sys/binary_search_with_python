@echo off
echo ============================================
echo NEON SURGE - Game Builder
echo ============================================
echo.

REM Check if pygame is installed
python -m pip list | find "pygame" > nul
if errorlevel 1 (
    echo Installing pygame...
    python -m pip install pygame
) else (
    echo pygame is already installed
)

echo.
echo Installing PyInstaller...
python -m pip install pyinstaller

echo.
echo Building NEON SURGE.exe...
pyinstaller --onefile --windowed --name "NEON SURGE" --icon=ICON.ico game.py 2>nul || pyinstaller --onefile --windowed --name "NEON SURGE" game.py

echo.
echo ============================================
echo Build Complete!
echo ============================================
echo.
echo Your executable is ready at:
echo dist\NEON SURGE.exe
echo.
pause
