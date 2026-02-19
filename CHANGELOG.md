# Changelog

Semua perubahan yang signifikan pada proyek ini akan didokumentasikan di file ini.

Format berdasarkan [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
dan proyek ini mengikuti [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Plugin system dengan auto-discovery
- Database SQLite untuk tracking user dan statistik
- Logging system dengan warna
- Pagination untuk daftar plugin

## [1.0.0] - 2024-XX-XX

### Added

#### Core Features
- **Plugin System** - Sistem plugin modular dengan auto-discovery
- **Plugin Manager** - Load, unload, dan reload plugin secara dinamis
- **Plugin Base Class** - Base class untuk semua plugin dengan metadata
- **Database Handler** - SQLite database untuk user tracking dan statistik
- **Logger** - Logging system dengan warna di terminal

#### Built-in Plugins
- **Start Plugin** - `/start`, `/menu` - Menu utama dan welcome message
- **Plugins Menu Plugin** - `/plugins` - Daftar plugin dengan pagination
- **Help Plugin** - `/help`, `/help [plugin]` - Sistem bantuan
- **Info Plugin** - `/info`, `/stats`, `/ping` - Informasi dan statistik bot
- **Echo Plugin** - `/echo`, `/upper`, `/lower`, `/reverse` - Text manipulation
- **Admin Plugin** - `/broadcast`, `/users`, `/reload`, `/logs` - Admin commands
- **Fun Plugin** - `/roll`, `/flip`, `/joke`, `/8ball` - Entertainment commands

#### Commands
| Command | Deskripsi | Plugin |
|---------|-----------|--------|
| `/start` | Memulai bot | Start |
| `/menu` | Menu utama | Start |
| `/plugins` | Daftar plugin | Plugins Menu |
| `/help` | Bantuan umum | Help |
| `/help [plugin]` | Bantuan plugin | Help |
| `/info` | Info bot | Info |
| `/stats` | Statistik bot | Info |
| `/ping` | Cek latency | Info |
| `/echo [teks]` | Echo pesan | Echo |
| `/upper [teks]` | Huruf besar | Echo |
| `/lower [teks]` | Huruf kecil | Echo |
| `/reverse [teks]` | Balik teks | Echo |
| `/broadcast [pesan]` | Kirim broadcast | Admin |
| `/users` | Statistik user | Admin |
| `/reload` | Reload plugins | Admin |
| `/logs` | Lihat log | Admin |
| `/roll [sides]` | Roll dadu | Fun |
| `/flip` | Flip koin | Fun |
| `/joke` | Random joke | Fun |
| `/8ball [pertanyaan]` | Magic 8-ball | Fun |

#### Configuration
- Environment variables support via `.env` file
- Configurable plugin folder
- Configurable database path
- Configurable logging level
- Admin IDs configuration

#### Database Tables
- `users` - Data user dan aktivitas
- `chats` - Data chat grup
- `stats` - Statistik penggunaan command
- `plugins` - Data plugin dan penggunaan
- `settings` - Pengaturan bot

#### Documentation
- README.md dengan panduan lengkap
- CONTRIBUTING.md dengan panduan kontribusi
- Template plugin yang jelas
- Kode yang well-documented

### Security
- Admin-only commands untuk operasi sensitif
- User activity tracking
- Command usage logging

---

## Template untuk Update

### [X.Y.Z] - YYYY-MM-DD

#### Added
- Fitur baru yang ditambahkan

#### Changed
- Perubahan pada fitur yang sudah ada

#### Deprecated
- Fitur yang akan dihapus di versi berikutnya

#### Removed
- Fitur yang dihapus

#### Fixed
- Bug yang diperbaiki

#### Security
- Perbaikan keamanan

---

## Version History

- `1.0.0` - Initial release dengan sistem plugin modular

## Contributing to Changelog

Saat membuat Pull Request, tambahkan entry di bagian `[Unreleased]` dengan format:

```markdown
### [Type]
- Deskripsi singkat perubahan (#PR_NUMBER)
```

Types: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`
