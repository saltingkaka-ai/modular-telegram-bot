"""
========================================
Plugin: Admin
========================================
Nama: Admin
Deskripsi: Plugin untuk admin commands (broadcast, user management, dll)
Commands:
  - /broadcast [pesan]: Kirim pesan ke semua user (admin only)
  - /users: Lihat jumlah user (admin only)
  - /reload: Reload semua plugin (admin only)
  - /logs: Lihat log terakhir (admin only)
Contoh Penggunaan:
  - /broadcast Halo semua!
  - /users
  - /reload
  - /logs
========================================
"""

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from core.plugin_base import PluginBase
from config import ADMIN_IDS
from utils.database import db
from utils.logger import logger

class AdminPlugin(PluginBase):
    """Plugin untuk admin commands"""
    
    PLUGIN_NAME = "Admin"
    PLUGIN_DESCRIPTION = "Admin commands untuk mengelola bot"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "admin"
    
    COMMANDS = [
        {"command": "broadcast", "description": "[Admin] Kirim broadcast", "handler": "cmd_broadcast"},
        {"command": "users", "description": "[Admin] Lihat statistik user", "handler": "cmd_users"},
        {"command": "reload", "description": "[Admin] Reload plugins", "handler": "cmd_reload"},
        {"command": "logs", "description": "[Admin] Lihat log", "handler": "cmd_logs"}
    ]
    
    EXAMPLES = [
        "/broadcast Halo semua!",
        "/users",
        "/reload",
        "/logs"
    ]
    
    async def initialize(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    def is_admin(self, user_id: int) -> bool:
        """Cek apakah user adalah admin"""
        return user_id in ADMIN_IDS
    
    async def cmd_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /broadcast
        Format: /broadcast [pesan]
        Hanya untuk admin
        """
        user = update.effective_user
        
        if not self.is_admin(user.id):
            await update.message.reply_text(
                "⛔ <b>Akses Ditolak!</b>\n\n"
                "Command ini hanya untuk admin.",
                parse_mode="HTML"
            )
            return
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/broadcast [pesan]</code>\n\n"
                "<i>Contoh: /broadcast Halo semua!</i>",
                parse_mode="HTML"
            )
            return
        
        message = " ".join(context.args)
        
        # Kirim status
        status_msg = await update.message.reply_text(
            "📤 <b>Mengirim broadcast...</b>",
            parse_mode="HTML"
        )
        
        # Kirim broadcast
        from bot import bot
        result = await bot.send_broadcast(message)
        
        await status_msg.edit_text(
            f"✅ <b>Broadcast Selesai!</b>\n\n"
            f"📤 <b>Berhasil:</b> {result['success']}\n"
            f"❌ <b>Gagal:</b> {result['failed']}\n"
            f"📊 <b>Total:</b> {result['total']}",
            parse_mode="HTML"
        )
        
        logger.info(f"Broadcast sent by admin {user.id}: {result}")
    
    async def cmd_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /users
        Menampilkan statistik user
        Hanya untuk admin
        """
        user = update.effective_user
        
        if not self.is_admin(user.id):
            await update.message.reply_text(
                "⛔ <b>Akses Ditolak!</b>\n\n"
                "Command ini hanya untuk admin.",
                parse_mode="HTML"
            )
            return
        
        # Dapatkan statistik
        total_users = db.get_user_count()
        recent_stats = db.get_stats(days=7)
        
        # Dapatkan beberapa user terbaru
        recent_users = db.get_all_users(limit=5)
        
        text = f"""
👥 <b>Statistik User</b>

📊 <b>Total User:</b> {total_users}
📈 <b>User Aktif (7 hari):</b> {recent_stats['active_users']}

🆕 <b>User Terbaru:</b>
"""
        
        for u in recent_users:
            username = f"@{u['username']}" if u['username'] else "No username"
            name = f"{u['first_name'] or ''} {u['last_name'] or ''}".strip() or "Unknown"
            text += f"  • {name} ({username}) - ID: <code>{u['user_id']}</code>\n"
        
        await update.message.reply_text(text, parse_mode="HTML")
        
        logger.command_used("/users", user.id, user.username)
    
    async def cmd_reload(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /reload
        Reload semua plugin
        Hanya untuk admin
        """
        user = update.effective_user
        
        if not self.is_admin(user.id):
            await update.message.reply_text(
                "⛔ <b>Akses Ditolak!</b>\n\n"
                "Command ini hanya untuk admin.",
                parse_mode="HTML"
            )
            return
        
        status_msg = await update.message.reply_text(
            "🔄 <b>Reloading plugins...</b>",
            parse_mode="HTML"
        )
        
        from bot import bot
        
        # Unload semua handlers dari application
        # Note: Ini adalah cara sederhana, untuk production perlu lebih hati-hati
        
        # Reload plugins
        results = bot.plugin_manager.reload_all_plugins()
        
        success_count = sum(1 for v in results.values() if v)
        total_count = len(results)
        
        # Buat detail
        details = []
        for name, success in results.items():
            status = "✅" if success else "❌"
            details.append(f"  {status} {name}")
        
        await status_msg.edit_text(
            f"🔄 <b>Reload Selesai!</b>\n\n"
            f"✅ <b>Berhasil:</b> {success_count}/{total_count}\n\n"
            f"<b>Detail:</b>\n" + "\n".join(details),
            parse_mode="HTML"
        )
        
        logger.info(f"Plugins reloaded by admin {user.id}: {success_count}/{total_count}")
    
    async def cmd_logs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /logs
        Menampilkan log terakhir
        Hanya untuk admin
        """
        user = update.effective_user
        
        if not self.is_admin(user.id):
            await update.message.reply_text(
                "⛔ <b>Akses Ditolak!</b>\n\n"
                "Command ini hanya untuk admin.",
                parse_mode="HTML"
            )
            return
        
        # Baca log file
        log_file = "logs/bot.log"
        
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # Ambil 20 baris terakhir
                last_lines = lines[-20:] if len(lines) > 20 else lines
                log_content = "".join(last_lines)
            
            if not log_content.strip():
                log_content = "<i>Log kosong</i>"
            
            # Truncate jika terlalu panjang
            if len(log_content) > 3500:
                log_content = log_content[-3500:] + "\n... [truncated]"
            
            await update.message.reply_text(
                f"📋 <b>Log Terakhir:</b>\n\n"
                f"<pre>{log_content}</pre>",
                parse_mode="HTML"
            )
            
        except FileNotFoundError:
            await update.message.reply_text(
                "⚠️ <b>File log tidak ditemukan!</b>",
                parse_mode="HTML"
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Error membaca log:</b> <code>{str(e)}</code>",
                parse_mode="HTML"
            )
        
        logger.command_used("/logs", user.id, user.username)

# Instance plugin
plugin = AdminPlugin()
