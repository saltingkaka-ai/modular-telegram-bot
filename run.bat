@echo off
REM ============================================
REM Modular Telegram Bot - Launcher Script (Windows)
REM ============================================

echo 🚀 Starting Modular Telegram Bot...
echo ====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed!
    pause
    exit /b 1
)

REM Create necessary directories
echo 📁 Creating directories...
if not exist "data" mkdir data
if not exist "logs" mkdir logs

REM Check if virtual environment exists
if not exist "venv" (
    echo 🔄 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install -q -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  .env file not found!
    echo 📝 Please copy .env.example to .env and fill in your BOT_TOKEN
    echo.
    echo    copy .env.example .env
    echo    notepad .env
    echo.
    pause
    exit /b 1
)

REM Run the bot
echo 🤖 Starting bot...
echo ====================================
python bot.py

pause
