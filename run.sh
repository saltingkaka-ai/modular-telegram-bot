#!/bin/bash
# ============================================
# Modular Telegram Bot - Launcher Script
# ============================================

echo "🚀 Starting Modular Telegram Bot..."
echo "===================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed!"
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔄 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Please copy .env.example to .env and fill in your BOT_TOKEN"
    echo ""
    echo "   cp .env.example .env"
    echo "   nano .env"
    echo ""
    exit 1
fi

# Run the bot
echo "🤖 Starting bot..."
echo "===================================="
python3 bot.py
