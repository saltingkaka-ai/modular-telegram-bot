# Plugin Documentation

Dokumentasi lengkap untuk semua plugin yang tersedia di Modular Telegram Bot.

## Daftar Plugin

### Core Plugins

| Plugin | Kategori | Commands | Deskripsi |
|--------|----------|----------|-----------|
| [Start](#start) | info | `/start`, `/menu` | Menu utama dan welcome |
| [Plugins Menu](#plugins-menu) | info | `/plugins` | Daftar plugin dengan pagination |
| [Help](#help) | info | `/help` | Sistem bantuan |
| [Info](#info) | info | `/info`, `/stats`, `/ping` | Informasi dan statistik |

### Utility Plugins

| Plugin | Kategori | Commands | Deskripsi |
|--------|----------|----------|-----------|
| [Echo](#echo) | utility | `/echo`, `/upper`, `/lower`, `/reverse` | Text manipulation |

### Admin Plugins

| Plugin | Kategori | Commands | Deskripsi |
|--------|----------|----------|-----------|
| [Admin](#admin) | admin | `/broadcast`, `/users`, `/reload`, `/logs` | Admin commands |

### Fun Plugins

| Plugin | Kategori | Commands | Deskripsi |
|--------|----------|----------|-----------|
| [Fun](#fun) | fun | `/roll`, `/flip`, `/joke`, `/8ball` | Entertainment |

---

## Start

**Kategori:** `info`  
**Author:** System  
**Version:** 1.0

### Deskripsi

Plugin untuk menangani command `/start` dan menampilkan menu utama bot.

### Commands

#### `/start`

Memulai bot dan menampilkan welcome message dengan menu utama.

**Usage:**
```
/start
```

**Response:**
- Welcome message dengan info bot
- Menu dengan tombol: 📦 Plugins, ❓ Bantuan, ℹ️ Info, 📊 Statistik

#### `/menu`

Menampilkan menu utama.

**Usage:**
```
/menu
```

**Response:**
- Menu dengan tombol navigasi

### Callbacks

- `menu_main` - Kembali ke menu utama

---

## Plugins Menu

**Kategori:** `info`  
**Author:** System  
**Version:** 1.0

### Deskripsi

Plugin untuk menampilkan daftar plugin yang terinstall dengan sistem pagination.

### Commands

#### `/plugins`

Menampilkan daftar semua plugin yang terinstall.

**Usage:**
```
/plugins
```

**Response:**
- Daftar plugin dengan emoji kategori
- Pagination: ◀️ Prev | Halaman | ▶️ Next
- Tombol 🔙 Kembali

**Features:**
- Klik plugin untuk lihat detail
- Navigasi halaman dengan Prev/Next
- Auto-pagination (5 plugin per halaman)

### Callbacks

- `plugins_list_{page}` - Navigasi halaman
- `plugin_detail_{name}` - Lihat detail plugin

---

## Help

**Kategori:** `info`  
**Author:** System  
**Version:** 1.0

### Deskripsi

Sistem bantuan untuk melihat daftar command dan informasi plugin.

### Commands

#### `/help`

Menampilkan daftar semua command yang tersedia.

**Usage:**
```
/help
```

**Response:**
- Daftar semua command dari semua plugin

#### `/help [plugin]`

Menampilkan bantuan untuk plugin tertentu.

**Usage:**
```
/help start
/help plugins
```

**Response:**
- Informasi detail tentang plugin
- Daftar command plugin
- Contoh penggunaan

### Callbacks

- `menu_help` - Tampilkan help dari menu

---

## Info

**Kategori:** `info`  
**Author:** System  
**Version:** 1.0

### Deskripsi

Plugin untuk menampilkan informasi dan statistik bot.

### Commands

#### `/info`

Menampilkan informasi tentang bot.

**Usage:**
```
/info
```

**Response:**
- Nama bot
- Versi
- Author
- Uptime
- Jumlah plugin
- Total pengguna

#### `/stats`

Menampilkan statistik penggunaan bot.

**Usage:**
```
/stats
```

**Response:**
- Total command (7 hari terakhir)
- Pengguna aktif
- Command populer
- Plugin paling banyak digunakan

#### `/ping`

Cek latency bot.

**Usage:**
```
/ping
```

**Response:**
- Latency dalam ms
- Uptime bot

### Callbacks

- `menu_info` - Tampilkan info dari menu
- `menu_stats` - Tampilkan stats dari menu (dengan refresh)

---

## Echo

**Kategori:** `utility`  
**Author:** System  
**Version:** 1.0

### Deskripsi

Plugin untuk manipulasi teks: echo, uppercase, lowercase, reverse.

### Commands

#### `/echo`

Mengulang teks yang dikirim.

**Usage:**
```
/echo Halo dunia!
```

**Response:**
```
📢 Echo:
Halo dunia!
```

#### `/upper`

Mengubah teks menjadi huruf besar.

**Usage:**
```
/upper hello world
```

**Response:**
```
🔠 Uppercase:
HELLO WORLD
```

#### `/lower`

Mengubah teks menjadi huruf kecil.

**Usage:**
```
/lower HALLO WORLD
```

**Response:**
```
🔡 Lowercase:
hello world
```

#### `/reverse`

Membalik teks.

**Usage:**
```
/reverse Hello World
```

**Response:**
```
🔄 Reverse:
Original: Hello World
Reversed: dlroW olleH
```

---

## Admin

**Kategori:** `admin`  
**Author:** System  
**Version:** 1.0

### Deskripsi

Plugin untuk admin commands: broadcast, user management, reload plugin.

**Note:** Semua command ini hanya bisa digunakan oleh admin.

### Commands

#### `/broadcast`

Mengirim pesan ke semua user.

**Usage:**
```
/broadcast Halo semua! Ini pesan broadcast.
```

**Response:**
```
✅ Broadcast Selesai!

📤 Berhasil: 150
❌ Gagal: 5
📊 Total: 155
```

**Note:** Hanya admin yang bisa menggunakan command ini.

#### `/users`

Menampilkan statistik user.

**Usage:**
```
/users
```

**Response:**
- Total user
- User aktif (7 hari)
- 5 user terbaru

**Note:** Hanya admin yang bisa menggunakan command ini.

#### `/reload`

Reload semua plugin.

**Usage:**
```
/reload
```

**Response:**
```
🔄 Reload Selesai!

✅ Berhasil: 7/7

Detail:
  ✅ start
  ✅ plugins_menu
  ✅ help
  ✅ info
  ✅ echo
  ✅ admin
  ✅ fun
```

**Note:** Hanya admin yang bisa menggunakan command ini.

#### `/logs`

Menampilkan log terakhir.

**Usage:**
```
/logs
```

**Response:**
- 20 baris log terakhir

**Note:** Hanya admin yang bisa menggunakan command ini.

---

## Fun

**Kategori:** `fun`  
**Author:** System  
**Version:** 1.0

### Deskripsi

Plugin untuk entertainment: roll dice, flip coin, jokes, magic 8-ball.

### Commands

#### `/roll`

Roll dadu.

**Usage:**
```
/roll        # Roll 6-sided dice
/roll 20     # Roll 20-sided dice
```

**Response:**
```
🎲 Roll 6-sided dice:

Hasil: 4!
```

#### `/flip`

Flip koin (heads/tails).

**Usage:**
```
/flip
```

**Response:**
```
🪙 Coin Flip:

Hasil: 👑 Heads!
```

#### `/joke`

Random joke.

**Usage:**
```
/joke
```

**Response:**
```
😄 Random Joke:

Why don't scientists trust atoms? Because they make up everything! 😄
```

#### `/8ball`

Magic 8-ball untuk pertanyaan.

**Usage:**
```
/8ball Apakah aku akan sukses?
```

**Response:**
```
❓ Pertanyaan: Apakah aku akan sukses?

🎱 It is certain
```

---

## Membuat Plugin Baru

Untuk membuat plugin baru, lihat [CONTRIBUTING.md](CONTRIBUTING.md#membuat-plugin-baru).

### Quick Template

```python
"""
========================================
Plugin: MyPlugin
========================================
Nama: MyPlugin
Deskripsi: Deskripsi plugin
Commands:
  - /mycommand: Deskripsi command
Contoh Penggunaan:
  - /mycommand
========================================
"""

from telegram import Update
from telegram.ext import ContextTypes
from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger

class MyPlugin(PluginBase):
    PLUGIN_NAME = "MyPlugin"
    PLUGIN_DESCRIPTION = "Deskripsi plugin"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "Your Name"
    PLUGIN_CATEGORY = "utility"
    
    COMMANDS = [
        {"command": "mycommand", "description": "Deskripsi", "handler": "cmd_mycommand"}
    ]
    
    EXAMPLES = ["/mycommand"]
    
    async def initialize(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    async def cmd_mycommand(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        db.update_user_activity(user.id)
        logger.command_used("/mycommand", user.id, user.username)
        await update.message.reply_text("Hello! 👋")

plugin = MyPlugin()
```

---

## Plugin Categories

| Kategori | Emoji | Deskripsi |
|----------|-------|-----------|
| admin | 👮 | Commands untuk admin |
| fun | 🎮 | Entertainment & games |
| utility | 🛠️ | Tools & utilities |
| info | 📊 | Information & stats |
| media | 🎵 | Media processing |
| other | 📦 | Lainnya |

---

## Changelog Plugin

### v1.0.0

- Initial release dengan 7 built-in plugins
- Sistem pagination untuk daftar plugin
- Auto-discovery plugin

---

## Contributing

Ingin menambahkan plugin baru? Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk panduan lengkap.
