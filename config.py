"""
========================================
Modular Telegram Bot - Configuration
========================================
Nama: Config
Deskripsi: File konfigurasi utama untuk bot
Command: -
Usage: Import dari file lain
========================================
"""

import os
from typing import Dict, Any

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv tidak terinstall, gunakan os.environ saja

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
BOT_NAME = os.getenv("BOT_NAME", "ModularBot")
BOT_VERSION = "1.0.0"
BOT_AUTHOR = "Developer"

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/bot_database.db")

# Plugin Configuration
PLUGINS_FOLDER = "plugins"
PLUGINS_PER_PAGE = 5

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/bot.log")

# Admin Configuration
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(","))) if os.getenv("ADMIN_IDS") else []

# Extra Features
ENABLE_STATS = True
ENABLE_BROADCAST = True
AUTO_DELETE_COMMANDS = False

# Message Templates
WELCOME_MESSAGE = """
👋 <b>Selamat datang di {bot_name}!</b>

🤖 <b>Versi:</b> {version}
📦 <b>Plugin terinstall:</b> {plugin_count}

<i>Bot modular yang mudah dikembangkan!</i>
"""

HELP_MESSAGE = """
📖 <b>Bantuan Penggunaan</b>

Gunakan tombol di bawah untuk navigasi:
• 📦 <b>Plugins</b> - Lihat semua plugin tersedia
• ❓ <b>Bantuan</b> - Panduan penggunaan
• ℹ️ <b>Info</b> - Informasi bot

Atau gunakan command /help untuk bantuan lengkap.
"""

# Button Labels
BUTTON_PLUGINS = "📦 Plugins"
BUTTON_HELP = "❓ Bantuan"
BUTTON_INFO = "ℹ️ Info"
BUTTON_BACK = "🔙 Kembali"
BUTTON_PREV = "◀️ Prev"
BUTTON_NEXT = "▶️ Next"
BUTTON_REFRESH = "🔄 Refresh"
BUTTON_CLOSE = "❌ Tutup"

# Emoji Collections
EMOJI_PLUGINS = {
    "admin": "👮",
    "fun": "🎮",
    "utility": "🛠️",
    "info": "📊",
    "media": "🎵",
    "other": "📦"
}

def get_config() -> Dict[str, Any]:
    """Mengembalikan semua konfigurasi dalam dictionary"""
    return {
        "bot_name": BOT_NAME,
        "bot_version": BOT_VERSION,
        "bot_author": BOT_AUTHOR,
        "plugins_per_page": PLUGINS_PER_PAGE,
        "admin_ids": ADMIN_IDS,
        "enable_stats": ENABLE_STATS,
        "enable_broadcast": ENABLE_BROADCAST
    }
