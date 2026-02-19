# Frequently Asked Questions (FAQ)

Pertanyaan yang sering ditanyakan tentang Modular Telegram Bot.

## General Questions

### Q: Apa itu Modular Telegram Bot?

**A:** Modular Telegram Bot adalah bot Telegram yang dibangun dengan sistem plugin modular. Ini berarti Anda bisa dengan mudah menambahkan, menghapus, atau memodifikasi fitur bot tanpa harus mengubah kode utama.

### Q: Apa keuntungan menggunakan sistem plugin?

**A:** 
- **Mudah dikembangkan** - Tambah fitur baru hanya dengan membuat file plugin
- **Modular** - Setiap fitur terpisah, tidak saling mengganggu
- **Reusable** - Plugin bisa digunakan di bot lain
- **Maintainable** - Kode lebih terorganisir dan mudah di-maintain

### Q: Apakah bot ini gratis?

**A:** Ya, bot ini open source dan gratis untuk digunakan. Lihat [LICENSE](LICENSE) untuk detail lisensi.

## Installation & Setup

### Q: Python versi berapa yang diperlukan?

**A:** Python 3.8 atau lebih tinggi.

### Q: Bagaimana cara mendapatkan bot token?

**A:**
1. Buka Telegram dan cari [@BotFather](https://t.me/BotFather)
2. Kirim `/newbot`
3. Ikuti instruksi
4. Copy token yang diberikan

### Q: Bot tidak berjalan, apa yang salah?

**A:** Cek hal berikut:
- Token sudah benar di `.env`
- Dependencies sudah terinstall (`pip install -r requirements.txt`)
- Python version 3.8+
- Virtual environment sudah diaktifkan

### Q: Bagaimana cara menjalankan bot di background?

**A:**

**Linux (systemd):**
```bash
# Buat service file
sudo nano /etc/systemd/system/modular-bot.service
```

```ini
[Unit]
Description=Modular Telegram Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/modular-telegram-bot
ExecStart=/path/to/modular-telegram-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable modular-bot
sudo systemctl start modular-bot
sudo systemctl status modular-bot
```

**Docker:**
```bash
docker-compose up -d
```

**Screen/Tmux:**
```bash
screen -S bot
python bot.py
# Press Ctrl+A, then D to detach
```

## Plugin Development

### Q: Bagaimana cara membuat plugin baru?

**A:** Lihat [CONTRIBUTING.md](CONTRIBUTING.md#membuat-plugin-baru) untuk panduan lengkap. Ringkasnya:

1. Buat file di `plugins/nama_plugin.py`
2. Extend class `PluginBase`
3. Implementasikan methods yang diperlukan
4. Buat instance plugin

### Q: Apa saja kategori plugin yang tersedia?

**A:**
- `admin` - Admin commands
- `fun` - Entertainment & games
- `utility` - Tools & utilities
- `info` - Information & stats
- `media` - Media processing
- `other` - Lainnya

### Q: Bagaimana cara reload plugin tanpa restart bot?

**A:** Gunakan command `/reload` (admin only) atau restart bot.

### Q: Apakah plugin bisa mengakses database?

**A:** Ya, gunakan `from utils.database import db` untuk mengakses database.

### Q: Bagaimana cara logging di plugin?

**A:** Gunakan `from utils.logger import logger`:

```python
logger.info("Pesan info")
logger.error("Pesan error")
logger.command_used("/command", user_id, username)
```

## Configuration

### Q: Bagaimana cara menambahkan admin?

**A:**
1. Dapatkan user ID dari [@userinfobot](https://t.me/userinfobot)
2. Tambahkan ke `ADMIN_IDS` di `.env`:
```bash
ADMIN_IDS=123456789,987654321
```
3. Restart bot

### Q: Bagaimana cara mengubah database path?

**A:** Edit `DATABASE_PATH` di `.env`:
```bash
DATABASE_PATH=/path/to/your/database.db
```

### Q: Bagaimana cara mengubah log level?

**A:** Edit `LOG_LEVEL` di `.env`:
```bash
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR
```

## Usage

### Q: Command apa saja yang tersedia?

**A:** Kirim `/help` untuk melihat semua command. Atau `/plugins` untuk melihat daftar plugin.

### Q: Bagaimana cara broadcast pesan ke semua user?

**A:** Gunakan `/broadcast [pesan]` (admin only).

### Q: Bagaimana cara melihat statistik bot?

**A:** Gunakan `/stats` untuk melihat statistik penggunaan.

### Q: Bagaimana cara cek latency bot?

**A:** Gunakan `/ping`.

## Troubleshooting

### Q: "ModuleNotFoundError" saat run bot

**A:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Q: Database locked error

**A:**
```bash
# Matikan bot
pkill -f bot.py

# Hapus journal file
rm data/*.db-journal

# Jalankan ulang
python bot.py
```

### Q: Bot tidak merespon command

**A:** Cek:
- Bot token benar
- Bot tidak blocked oleh user
- Bot memiliki permission di grup (jika di grup)
- Tidak ada error di log (`logs/bot.log`)

### Q: Plugin tidak terdeteksi

**A:** Cek:
- File plugin di folder `plugins/`
- Nama file berakhiran `.py`
- Ada `plugin = MyPlugin()` di akhir file
- Class meng-extend `PluginBase`

## Advanced

### Q: Bagaimana cara deploy ke server?

**A:** Lihat [INSTALL.md](INSTALL.md#running-the-bot) untuk berbagai metode deployment.

### Q: Apakah bisa menggunakan database lain selain SQLite?

**A:** Bisa, tapi perlu modifikasi `utils/database.py`. Bot menggunakan SQLite karena simple dan tidak perlu setup tambahan.

### Q: Bagaimana cara scale bot untuk banyak user?

**A:**
- Gunakan database yang lebih powerful (PostgreSQL, MySQL)
- Implementasi caching (Redis)
- Gunakan message queue untuk broadcast
- Deploy multiple instances dengan load balancer

### Q: Apakah bot support webhook?

**A:** Saat ini bot menggunakan polling. Untuk webhook, perlu modifikasi di `bot.py`.

### Q: Bagaimana cara kontribusi ke proyek ini?

**A:** Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk panduan lengkap.

## Still Have Questions?

Jika FAQ ini tidak menjawab pertanyaan Anda:

1. Baca [README.md](README.md) dan [INSTALL.md](INSTALL.md)
2. Cari di [Issues](../../issues)
3. Buat [new issue](../../issues/new) dengan label `question`
4. Join [Discussions](../../discussions)

---

**Note:** FAQ ini akan terus diupdate. Jika ada pertanyaan yang sering ditanyakan, silakan suggest untuk ditambahkan.
