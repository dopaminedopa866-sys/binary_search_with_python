# NEON SURGE - Setup & Build Guide

## Quick Start

### Option 1: Run Game Directly (Fastest)
```bash
pip install pygame
python game.py
```

Or simply double-click `RUN_GAME.bat`

### Option 2: Build Executable (.exe)

#### Method A - Automatic (Easiest)
Double-click: `BUILD_EXE.bat`

This will:
1. Install pygame if needed
2. Install PyInstaller
3. Build game.exe automatically
4. Output to `dist/NEON SURGE.exe`

#### Method B - Manual Command Line
```bash
pip install pygame pyinstaller
pyinstaller --onefile --windowed --name "NEON SURGE" game.py
```

## System Requirements
- Python 3.8+
- 100MB disk space for build
- Windows/Mac/Linux

## Game Features
🎮 **Gameplay**
- Wave-based enemy combat
- Three unique enemy types
- Particle explosion effects
- Progressive difficulty

🎨 **Visuals**
- Neon cyberpunk aesthetic
- Glowing effects and animations
- Grid-based background
- Real-time particle system

📊 **Features**
- Health tracking system
- Wave progression counter
- Score accumulation
- Smooth 60 FPS performance

## Controls
- ⬅️➡️⬆️⬇️ or **WASD** - Move
- 🖱️ **Click** - Shoot
- **ESC** - Exit
- **R** - Restart (after game over)

## Troubleshooting

### pygame not found
```bash
pip install pygame --upgrade
```

### PyInstaller not creating exe
```bash
pip install pyinstaller --upgrade
pyinstaller --onefile --windowed game.py
```

### Permission denied on .bat files
Right-click → Run as Administrator

## After Building
- Your executable will be in the `dist/` folder
- Can be distributed standalone
- No Python installation required on target machine

Enjoy playing NEON SURGE! 🚀
