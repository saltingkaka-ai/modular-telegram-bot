# Contributing to Modular Telegram Bot

Terima kasih atas minat Anda untuk berkontribusi pada **Modular Telegram Bot**! Kami sangat menghargai setiap kontribusi, baik itu bug report, feature request, dokumentasi, atau code contribution.

## Daftar Isi

- [Code of Conduct](#code-of-conduct)
- [Cara Berkontribusi](#cara-berkontribusi)
  - [Melaporkan Bug](#melaporkan-bug)
  - [Mengusulkan Fitur Baru](#mengusulkan-fitur-baru)
  - [Membuat Plugin Baru](#membuat-plugin-baru)
  - [Pull Request](#pull-request)
- [Development Setup](#development-setup)
- [Style Guide](#style-guide)
- [Commit Message Guidelines](#commit-message-guidelines)

## Code of Conduct

Proyek ini dan semua yang berpartisipasi di dalamnya harus mengikuti [Code of Conduct](CODE_OF_CONDUCT.md).

## Cara Berkontribusi

### Melaporkan Bug

Jika Anda menemukan bug, silakan buat [issue baru](../../issues/new?template=bug_report.md) dengan informasi berikut:

- **Deskripsi jelas** tentang bug apa yang terjadi
- **Langkah reproduksi** - langkah-langkah untuk memunculkan bug
- **Expected behavior** - apa yang seharusnya terjadi
- **Screenshots** - jika memungkinkan
- **Environment:**
  - OS: [e.g. Ubuntu 20.04]
  - Python version: [e.g. 3.9]
  - Bot version: [e.g. 1.0.0]
- **Log error** - copy paste log error jika ada

### Mengusulkan Fitur Baru

Untuk mengusulkan fitur baru, buat [issue baru](../../issues/new?template=feature_request.md) dengan format:

- **Deskripsi fitur** - jelaskan fitur yang diinginkan
- **Use case** - bagaimana fitur ini akan digunakan
- **Alternatif** - apakah ada alternatif lain yang sudah dicoba
- **Additional context** - informasi tambahan

### Membuat Plugin Baru

Ini adalah cara paling mudah untuk berkontribusi! Ikuti langkah-langkah berikut:

1. **Fork repository** ini
2. **Buat branch baru** untuk plugin Anda:
   ```bash
   git checkout -b plugin/nama-plugin
   ```
3. **Buat file plugin** di folder `plugins/`:
   ```bash
   touch plugins/nama_plugin.py
   ```
4. **Ikuti template plugin** (lihat di bawah)
5. **Test plugin Anda** secara lokal
6. **Commit dan push** perubahan
7. **Buat Pull Request**

#### Template Plugin

```python
"""
========================================
Plugin: NamaPlugin
========================================
Nama: NamaPlugin
Deskripsi: Deskripsi singkat plugin
Commands:
  - /command1: Deskripsi command 1
  - /command2: Deskripsi command 2
Contoh Penggunaan:
  - /command1 arg1
  - /command2
========================================
"""

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger

class NamaPlugin(PluginBase):
    """Deskripsi lengkap plugin"""
    
    PLUGIN_NAME = "NamaPlugin"
    PLUGIN_DESCRIPTION = "Deskripsi singkat plugin"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "Your Name"
    PLUGIN_CATEGORY = "utility"  # Pilih: admin, fun, utility, info, media, other
    
    COMMANDS = [
        {"command": "command1", "description": "Deskripsi command 1", "handler": "cmd_command1"},
        {"command": "command2", "description": "Deskripsi command 2", "handler": "cmd_command2"}
    ]
    
    EXAMPLES = [
        "/command1 arg1",
        "/command2"
    ]
    
    def __init__(self):
        super().__init__()
        # Tambahkan callback handlers jika diperlukan
        # self.add_handler(CallbackQueryHandler(self.my_callback, pattern="^pattern_"))
    
    async def initialize(self):
        """Dipanggil saat plugin di-load"""
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        """Dipanggil saat plugin di-unload"""
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    async def cmd_command1(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk command /command1"""
        user = update.effective_user
        db.update_user_activity(user.id)
        logger.command_used("/command1", user.id, user.username)
        
        # Your code here
        await update.message.reply_text("Response dari command1!")
    
    async def cmd_command2(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk command /command2"""
        user = update.effective_user
        db.update_user_activity(user.id)
        logger.command_used("/command2", user.id, user.username)
        
        # Your code here
        await update.message.reply_text("Response dari command2!")

# WAJIB: Buat instance plugin
plugin = NamaPlugin()
```

#### Kategori Plugin

| Kategori | Emoji | Deskripsi |
|----------|-------|-----------|
| `admin` | 👮 | Commands untuk admin |
| `fun` | 🎮 | Entertainment & games |
| `utility` | 🛠️ | Tools & utilities |
| `info` | 📊 | Information & stats |
| `media` | 🎵 | Media processing |
| `other` | 📦 | Lainnya |

### Pull Request

1. **Update README.md** jika menambahkan fitur baru
2. **Update CHANGELOG.md** dengan perubahan Anda
3. **Pastikan test berjalan** (jika ada)
4. **Deskripsi PR yang jelas** - jelaskan apa yang diubah dan mengapa

## Development Setup

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Setup

```bash
# 1. Fork dan clone repository
git clone https://github.com/YOUR_USERNAME/modular-telegram-bot.git
cd modular-telegram-bot

# 2. Buat virtual environment
python -m venv venv

# 3. Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Copy environment file
cp .env.example .env

# 6. Edit .env dengan token bot Anda
nano .env

# 7. Jalankan bot
python bot.py
```

## Style Guide

### Python Code Style

Ikuti [PEP 8](https://pep8.org/) dengan beberapa penyesuaian:

- **Indentasi**: 4 spaces (bukan tabs)
- **Line length**: Maksimal 100 karakter
- **Docstrings**: Gunakan triple quotes dengan format yang jelas
- **Type hints**: Gunakan type hints untuk parameter dan return value
- **Naming**:
  - `snake_case` untuk functions dan variables
  - `PascalCase` untuk classes
  - `UPPER_CASE` untuk constants

### Contoh Kode yang Baik

```python
from typing import Optional, List
from telegram import Update
from telegram.ext import ContextTypes

async def process_message(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    message_text: Optional[str] = None
) -> bool:
    """
    Memproses pesan dari user.
    
    Args:
        update: Update object dari Telegram
        context: Context object
        user_id: ID user yang mengirim pesan
        message_text: Isi pesan (optional)
    
    Returns:
        True jika berhasil diproses, False jika gagal
    """
    if not message_text:
        return False
    
    # Process message
    processed = message_text.strip().lower()
    
    return len(processed) > 0
```

### Plugin Structure

```python
"""
========================================
Plugin: NamaPlugin
========================================
Nama: NamaPlugin
Deskripsi: Deskripsi singkat
Commands:
  - /command: Deskripsi
Contoh Penggunaan:
  - /command
========================================
"""

# 1. Imports (urutkan: stdlib, third-party, local)
import os
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger

# 2. Class definition
class NamaPlugin(PluginBase):
    # 3. Metadata (WAJIB)
    PLUGIN_NAME = "NamaPlugin"
    PLUGIN_DESCRIPTION = "Deskripsi"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "Your Name"
    PLUGIN_CATEGORY = "utility"
    
    # 4. Commands
    COMMANDS = [...]
    EXAMPLES = [...]
    
    # 5. Methods
    async def initialize(self): ...
    async def shutdown(self): ...
    async def cmd_command(self, update, context): ...

# 6. Instance (WAJIB)
plugin = NamaPlugin()
```

## Commit Message Guidelines

Gunakan format commit message yang jelas:

```
<type>: <subject>

<body> (optional)

<footer> (optional)
```

### Types

- **feat**: Fitur baru
- **fix**: Bug fix
- **docs**: Perubahan dokumentasi
- **style**: Formatting, missing semi colons, etc; no code change
- **refactor**: Refactoring code
- **test**: Menambah test
- **chore**: Update build tasks, package manager configs, etc

### Contoh

```
feat: add weather plugin

- Add /weather command to get current weather
- Support multiple cities
- Cache results for 10 minutes

Closes #123
```

```
fix: handle empty message in echo plugin

- Check if args is empty before processing
- Return helpful error message

Fixes #456
```

```
docs: update README with new plugin guide

- Add step-by-step plugin creation guide
- Add troubleshooting section
```

## Pertanyaan?

Jika ada pertanyaan, silakan:

1. Baca [README.md](README.md) terlebih dahulu
2. Cari di [Issues](../../issues) yang sudah ada
3. Buat [issue baru](../../issues/new) dengan label `question`

Terima kasih telah berkontribusi! 🎉
