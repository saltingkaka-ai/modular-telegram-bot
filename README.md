### NOT UPDATED!!!

# Modular Telegram Bot

Bot Telegram modular yang mudah dikembangkan dengan sistem plugin yang powerful.

## Fitur Utama

- **Sistem Plugin Modular** - Tambah/hapus fitur dengan mudah
- **Auto-Discovery Plugin** - Plugin otomatis terdeteksi dan diload
- **Pagination** - Navigasi plugin dengan sistem halaman
- **Database SQLite** - Penyimpanan data user dan statistik
- **Logging System** - Logging dengan warna di terminal
- **Admin Commands** - Broadcast, user management, reload plugin
- **Statistik Real-time** - Pantau penggunaan bot

## Struktur Proyek

```
modular_telegram_bot/
├── bot.py                 # File utama bot
├── config.py              # Konfigurasi bot
├── requirements.txt       # Dependencies
├── README.md             # Dokumentasi
├── core/                 # Core functionality
│   ├── __init__.py
│   ├── plugin_base.py    # Base class untuk plugin
│   └── plugin_manager.py # Manager untuk plugin
├── utils/                # Utilities
│   ├── __init__.py
│   ├── database.py       # Database handler
│   └── logger.py         # Logging system
├── plugins/              # Folder plugin
│   ├── __init__.py
│   ├── start.py          # Plugin start & menu
│   ├── plugins_menu.py   # Plugin list dengan pagination
│   ├── help.py           # Help system
│   ├── info.py           # Info & stats
│   ├── echo.py           # Echo & text manipulation
│   ├── admin.py          # Admin commands
│   └── fun.py            # Fun commands
├── data/                 # Database folder
└── logs/                 # Log files
```

## Cara Menggunakan

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Konfigurasi Bot Token

Edit `config.py` dan ganti `YOUR_BOT_TOKEN_HERE` dengan token bot Anda:

```python
BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrSTUvwxyz"
```

Atau set environment variable:

```bash
export BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrSTUvwxyz"
```

### 3. Jalankan Bot

```bash
python bot.py
```

## Membuat Plugin Baru

### Template Plugin

Buat file baru di folder `plugins/` (contoh: `myplugin.py`):

```python
"""
========================================
Plugin: MyPlugin
========================================
Nama: MyPlugin
Deskripsi: Deskripsi plugin Anda
Commands:
  - /mycommand: Deskripsi command
Contoh Penggunaan:
  - /mycommand arg1 arg2
========================================
"""

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger

class MyPlugin(PluginBase):
    """Deskripsi plugin"""
    
    # Metadata plugin (WAJIB)
    PLUGIN_NAME = "MyPlugin"
    PLUGIN_DESCRIPTION = "Deskripsi plugin Anda"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "Your Name"
    PLUGIN_CATEGORY = "utility"  # admin, fun, utility, info, media, other
    
    # Daftar commands yang disediakan
    COMMANDS = [
        {
            "command": "mycommand", 
            "description": "Deskripsi command", 
            "handler": "cmd_mycommand"
        }
    ]
    
    # Contoh penggunaan
    EXAMPLES = [
        "/mycommand arg1 arg2"
    ]
    
    def __init__(self):
        super().__init__()
        # Tambahkan custom handlers jika perlu
        # self.add_handler(CallbackQueryHandler(self.my_callback, pattern="^my_pattern"))
    
    async def initialize(self):
        """Dipanggil saat plugin di-load"""
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        """Dipanggil saat plugin di-unload"""
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    async def cmd_mycommand(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk command /mycommand"""
        user = update.effective_user
        
        # Update aktivitas user
        db.update_user_activity(user.id)
        
        # Log command
        logger.command_used("/mycommand", user.id, user.username)
        
        # Kirim respons
        await update.message.reply_text(
            "Hello from MyPlugin! 👋",
            parse_mode="HTML"
        )

# Instance plugin (WAJIB)
plugin = MyPlugin()
```

### Kategori Plugin

- `admin` - Commands untuk admin
- `fun` - Fitur entertainment
- `utility` - Tools dan utilitas
- `info` - Informasi dan statistik
- `media` - Media processing
- `other` - Lainnya

## Commands Tersedia

### General Commands
| Command | Deskripsi |
|---------|-----------|
| `/start` | Memulai bot |
| `/menu` | Menampilkan menu utama |
| `/help` | Bantuan umum |
| `/help [plugin]` | Bantuan untuk plugin tertentu |
| `/plugins` | Daftar plugin |
| `/info` | Informasi bot |
| `/stats` | Statistik bot |
| `/ping` | Cek latency |

### Utility Commands
| Command | Deskripsi |
|---------|-----------|
| `/echo [teks]` | Mengulang teks |
| `/upper [teks]` | Huruf besar |
| `/lower [teks]` | Huruf kecil |
| `/reverse [teks]` | Membalik teks |

### Fun Commands
| Command | Deskripsi |
|---------|-----------|
| `/roll [sides]` | Roll dadu |
| `/flip` | Flip koin |
| `/joke` | Random joke |
| `/8ball [pertanyaan]` | Magic 8-ball |

### Admin Commands
| Command | Deskripsi |
|---------|-----------|
| `/broadcast [pesan]` | Kirim ke semua user |
| `/users` | Statistik user |
| `/reload` | Reload plugins |
| `/logs` | Lihat log |

## Konfigurasi

Edit `config.py` untuk mengubah pengaturan:

```python
# Bot Configuration
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Token dari @BotFather
BOT_NAME = "ModularBot"
BOT_VERSION = "1.0.0"

# Admin IDs (untuk admin commands)
ADMIN_IDS = [123456789, 987654321]  # Ganti dengan user ID admin

# Plugin Configuration
PLUGINS_PER_PAGE = 5  # Jumlah plugin per halaman

# Database
DATABASE_PATH = "data/bot_database.db"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "logs/bot.log"
```

## Database

Bot menggunakan SQLite dengan tabel:

- **users** - Data user
- **chats** - Data chat grup
- **stats** - Statistik command
- **plugins** - Data plugin
- **settings** - Pengaturan bot

## Menambahkan Admin

1. Dapatkan user ID Anda dari @userinfobot
2. Tambahkan ke `ADMIN_IDS` di `config.py`:

```python
ADMIN_IDS = [123456789]  # Ganti dengan ID Anda
```

## Tips Pengembangan

1. **Reload Plugin** - Gunakan `/reload` untuk reload plugin tanpa restart bot
2. **Log** - Cek `logs/bot.log` untuk melihat aktivitas bot
3. **Database** - Gunakan `db` object untuk akses database
4. **Logger** - Gunakan `logger` untuk logging

## Troubleshooting

### Bot tidak berjalan
- Pastikan token sudah benar
- Pastikan dependencies sudah terinstall

### Plugin tidak terdeteksi
- Pastikan file plugin ada di folder `plugins/`
- Pastikan nama file berakhiran `.py`
- Pastikan ada `plugin = MyPlugin()` di akhir file

### Error saat load plugin
- Cek log di `logs/bot.log`
- Pastikan class meng-extend `PluginBase`
- Pastikan `PLUGIN_NAME` sudah diisi

## License

MIT License - Bebas digunakan dan dimodifikasi.

---

**Selamat mencoba!** 🚀
