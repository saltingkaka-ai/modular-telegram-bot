# Installation Guide

Panduan lengkap untuk menginstall dan menjalankan Modular Telegram Bot.

## Daftar Isi

- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
  - [Method 1: Using pip (Recommended)](#method-1-using-pip-recommended)
  - [Method 2: From Source](#method-2-from-source)
  - [Method 3: Using Docker](#method-3-using-docker)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- A Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))

## Installation Methods

### Method 1: Using pip (Recommended)

```bash
# Install from PyPI (when published)
pip install modular-telegram-bot

# Or install from source
pip install git+https://github.com/YOUR_USERNAME/modular-telegram-bot.git
```

### Method 2: From Source

#### Linux/macOS

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/modular-telegram-bot.git
cd modular-telegram-bot

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
cp .env.example .env

# 5. Edit .env with your bot token
nano .env
# or
vim .env
```

#### Windows

```powershell
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/modular-telegram-bot.git
cd modular-telegram-bot

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
copy .env.example .env

# 5. Edit .env with your bot token
notepad .env
```

### Method 3: Using Docker

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/modular-telegram-bot.git
cd modular-telegram-bot

# 2. Create .env file
cp .env.example .env
# Edit .env with your bot token

# 3. Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t modular-bot .
docker run -d --env-file .env -v $(pwd)/data:/app/data -v $(pwd)/logs:/app/logs modular-bot
```

#### Docker Commands

```bash
# Start bot
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop bot
docker-compose down

# Restart bot
docker-compose restart

# Update bot
docker-compose pull
docker-compose up -d

# Backup database
docker-compose --profile backup run backup
```

## Configuration

### Required Configuration

Edit `.env` file dengan konfigurasi berikut:

```bash
# WAJIB: Token bot dari @BotFather
BOT_TOKEN=your_bot_token_here

# Optional: Nama bot
BOT_NAME=MyModularBot

# Optional: Admin IDs (pisahkan dengan koma)
ADMIN_IDS=123456789,987654321

# Optional: Database path
DATABASE_PATH=data/bot_database.db

# Optional: Log level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Optional: Log file path
LOG_FILE=logs/bot.log
```

### Getting Bot Token

1. Buka Telegram dan cari [@BotFather](https://t.me/BotFather)
2. Kirim `/newbot`
3. Ikuti instruksi untuk membuat bot baru
4. Copy token yang diberikan
5. Paste ke `.env` file

### Getting Admin ID

1. Buka Telegram dan cari [@userinfobot](https://t.me/userinfobot)
2. Kirim pesan apa saja
3. Bot akan reply dengan informasi user ID Anda
4. Copy ID tersebut ke `ADMIN_IDS` di `.env`

## Running the Bot

### Using Makefile (Recommended)

```bash
# Setup everything
make setup

# Run bot
make run

# Other commands
make help  # Show all available commands
```

### Using Scripts

```bash
# Linux/macOS
./run.sh

# Windows
run.bat
```

### Manual

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Run bot
python bot.py
```

### Using Docker

```bash
docker-compose up -d
```

## Troubleshooting

### Common Issues

#### 1. "BOT_TOKEN belum diatur!"

**Problem**: Token belum diatur di `.env` file

**Solution**:
```bash
# Pastikan .env file ada
cp .env.example .env

# Edit dan tambahkan token
nano .env
# BOT_TOKEN=your_actual_token_here
```

#### 2. "ModuleNotFoundError: No module named 'telegram'"

**Problem**: Dependencies belum terinstall

**Solution**:
```bash
pip install -r requirements.txt
```

#### 3. "Permission denied" saat run script

**Problem**: Script tidak executable

**Solution**:
```bash
chmod +x run.sh
```

#### 4. Database locked error

**Problem**: Database sedang digunakan proses lain

**Solution**:
```bash
# Matikan bot
pkill -f bot.py

# Hapus lock file (jika ada)
rm data/*.db-journal

# Jalankan ulang
python bot.py
```

#### 5. Docker: "Cannot connect to the Docker daemon"

**Problem**: Docker service tidak berjalan

**Solution**:
```bash
# Linux
sudo systemctl start docker

# macOS/Windows
# Buka Docker Desktop application
```

### Getting Help

Jika masalah masih berlanjut:

1. Check [Issues](../../issues) yang sudah ada
2. Buat [new issue](../../issues/new) dengan label `question`
3. Join diskusi di [Discussions](../../discussions)

## Next Steps

Setelah bot berjalan:

1. Buka Telegram dan cari bot Anda
2. Kirim `/start` untuk memulai
3. Explore commands dengan `/help`
4. Lihat daftar plugin dengan `/plugins`
5. Baca [CONTRIBUTING.md](CONTRIBUTING.md) untuk membuat plugin sendiri

## Uninstallation

### pip

```bash
pip uninstall modular-telegram-bot
```

### Source

```bash
# Hapus folder proyek
rm -rf modular-telegram-bot

# Hapus virtual environment
deactivate
rm -rf venv
```

### Docker

```bash
docker-compose down -v
docker rmi modular-telegram-bot
```
