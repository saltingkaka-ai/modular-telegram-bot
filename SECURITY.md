# Security Policy

## Supported Versions

Versi berikut saat ini menerima update keamanan:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Jika Anda menemukan kerentanan keamanan dalam proyek ini, harap ikuti langkah-langkah berikut:

### 1. Jangan Buat Public Issue

Jangan membuat public issue untuk melaporkan kerentanan keamanan. Ini bisa membahayakan user lain.

### 2. Hubungi Kami Secara Langsung

Kirim email ke [your-security-email@example.com] dengan informasi berikut:

- **Deskripsi kerentanan** - Jelaskan dengan jelas apa masalahnya
- **Langkah reproduksi** - Bagaimana kami bisa mereproduksi masalah ini
- **Impact** - Seberapa parah dampaknya
- **Suggested fix** (opsional) - Jika Anda punya ide untuk memperbaiki
- **Your contact** - Bagaimana kami bisa menghubungi Anda

### 3. Tunggu Respons

Kami akan merespons dalam:

- **24 jam** - Konfirmasi penerimaan laporan
- **72 jam** - Assessment awal dan rencana tindakan
- **7 hari** - Update progress perbaikan

### 4. Disclosure Policy

Kami mengikuti responsible disclosure:

1. Laporan diterima dan dikonfirmasi
2. Kerentanan dianalisis dan diverifikasi
3. Fix dikembangkan dan di-test
4. Fix dirilis dalam update
5. Laporan di-publish (dengan credit ke reporter)

## Security Best Practices untuk User

### Bot Token

- **Jangan pernah** commit bot token ke repository public
- Gunakan `.env` file atau environment variables
- Rotate token secara berkala
- Jika token bocor, segera revoke dan generate baru via @BotFather

### Admin Access

- Batasi admin IDs di `config.py`
- Jangan tambahkan user yang tidak dikenal sebagai admin
- Review admin list secara berkala

### Database

- Backup database secara berkala
- Jangan expose database file ke public
- Gunakan permission yang tepat untuk file database

### Dependencies

- Update dependencies secara berkala
- Gunakan `pip-audit` untuk cek kerentanan dependencies

```bash
pip install pip-audit
pip-audit
```

## Security Features

Proyek ini memiliki beberapa fitur keamanan:

- ✅ Admin-only commands untuk operasi sensitif
- ✅ User activity tracking
- ✅ Command usage logging
- ✅ Environment variables untuk secrets
- ✅ Input validation

## Known Security Considerations

### Current Limitations

1. **SQLite Database** - Database file bisa diakses jika server di-compromise
2. **Broadcast Feature** - Admin bisa kirim pesan ke semua user (gunakan dengan hati-hati)
3. **Plugin System** - Plugin bisa mengeksekusi kode arbitrary (hanya install plugin terpercaya)

### Mitigation

- Gunakan file permission yang tepat
- Batasi admin access
- Review plugin code sebelum install

## Security Update History

| Date | Version | Issue | Fix |
|------|---------|-------|-----|
| - | - | - | - |

## Credits

Terima kasih kepada semua yang telah membantu meningkatkan keamanan proyek ini.

---

Last updated: 2024
