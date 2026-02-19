"""
========================================
Plugin: Info
========================================
Nama: Info
Deskripsi: Plugin untuk menampilkan informasi tentang bot
Commands:
  - /info: Menampilkan informasi bot
  - /stats: Menampilkan statistik bot
  - /ping: Cek latency bot
Contoh Penggunaan:
  - /info
  - /stats
  - /ping
========================================
"""

import time
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from core.plugin_base import PluginBase
from config import BOT_NAME, BOT_VERSION, BOT_AUTHOR, BUTTON_BACK
from utils.database import db
from utils.logger import logger

class InfoPlugin(PluginBase):
    """Plugin untuk informasi dan statistik bot"""
    
    PLUGIN_NAME = "Info"
    PLUGIN_DESCRIPTION = "Informasi dan statistik bot"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "info"
    
    COMMANDS = [
        {"command": "info", "description": "Informasi tentang bot", "handler": "cmd_info"},
        {"command": "stats", "description": "Statistik bot", "handler": "cmd_stats"},
        {"command": "ping", "description": "Cek latency bot", "handler": "cmd_ping"}
    ]
    
    EXAMPLES = [
        "/info",
        "/stats",
        "/ping"
    ]
    
    # Waktu bot mulai (untuk uptime)
    _start_time = datetime.now()
    
    def __init__(self):
        super().__init__()
        self.add_handler(CallbackQueryHandler(self.cb_menu_info, pattern="^menu_info$"))
        self.add_handler(CallbackQueryHandler(self.cb_menu_stats, pattern="^menu_stats$"))
    
    async def initialize(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
        InfoPlugin._start_time = datetime.now()
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    def get_uptime(self) -> str:
        """Menghitung uptime bot"""
        now = datetime.now()
        diff = now - self._start_time
        
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days} hari")
        if hours > 0:
            parts.append(f"{hours} jam")
        if minutes > 0:
            parts.append(f"{minutes} menit")
        if seconds > 0 or not parts:
            parts.append(f"{seconds} detik")
        
        return ", ".join(parts)
    
    async def cmd_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /info
        Menampilkan informasi tentang bot
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        logger.command_used("/info", user.id, user.username)
        
        from bot import bot
        
        info_text = f"""
ℹ️ <b>Informasi Bot</b>

🤖 <b>Nama:</b> {BOT_NAME}
📌 <b>Versi:</b> <code>{BOT_VERSION}</code>
👤 <b>Author:</b> <code>{BOT_AUTHOR}</code>
⏱️ <b>Uptime:</b> {self.get_uptime()}

📦 <b>Plugin terinstall:</b> {bot.plugin_manager.plugin_count}
👥 <b>Total pengguna:</b> {db.get_user_count()}

<i>Bot modular yang mudah dikembangkan!</i>
"""
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Statistik", callback_data="menu_stats")],
            [InlineKeyboardButton(BUTTON_BACK, callback_data="menu_main")]
        ])
        
        await update.message.reply_text(info_text, parse_mode="HTML", reply_markup=keyboard)
    
    async def cmd_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /stats
        Menampilkan statistik bot
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        logger.command_used("/stats", user.id, user.username)
        
        await self._show_stats(update, context, is_callback=False)
    
    async def _show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool = False):
        """Helper untuk menampilkan statistik"""
        # Dapatkan statistik dari database
        stats = db.get_stats(days=7)
        
        # Statistik plugin
        plugin_stats = db.get_plugin_stats()
        
        stats_text = f"""
📊 <b>Statistik Bot</b>

<i>Periode: 7 hari terakhir</i>

📈 <b>Total Command:</b> {stats['total_commands']}
👥 <b>Pengguna Aktif:</b> {stats['active_users']}

🏆 <b>Command Populer:</b>
"""
        
        if stats['top_commands']:
            for i, cmd in enumerate(stats['top_commands'][:5], 1):
                stats_text += f"  {i}. /{cmd['command']} - {cmd['total']} kali\n"
        else:
            stats_text += "  <i>Belum ada data</i>\n"
        
        stats_text += f"\n📦 <b>Plugin Paling Banyak Digunakan:</b>\n"
        
        if plugin_stats:
            for i, plugin in enumerate(plugin_stats[:3], 1):
                stats_text += f"  {i}. {plugin['name']} - {plugin['usage_count']} kali\n"
        else:
            stats_text += "  <i>Belum ada data</i>\n"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="menu_stats")],
            [InlineKeyboardButton(BUTTON_BACK, callback_data="menu_main")]
        ])
        
        if is_callback:
            await update.callback_query.edit_message_text(stats_text, parse_mode="HTML", reply_markup=keyboard)
        else:
            await update.message.reply_text(stats_text, parse_mode="HTML", reply_markup=keyboard)
    
    async def cmd_ping(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /ping
        Cek latency bot
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        logger.command_used("/ping", user.id, user.username)
        
        # Hitung latency
        start_time = time.time()
        message = await update.message.reply_text("🏓 <b>Pong!</b>", parse_mode="HTML")
        end_time = time.time()
        
        latency_ms = round((end_time - start_time) * 1000, 2)
        
        # Edit pesan dengan latency
        await message.edit_text(
            f"🏓 <b>Pong!</b>\n\n"
            f"⚡ <b>Latency:</b> <code>{latency_ms}ms</code>\n"
            f"⏱️ <b>Uptime:</b> {self.get_uptime()}",
            parse_mode="HTML"
        )
    
    async def cb_menu_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk callback menu_info"""
        query = update.callback_query
        await query.answer()
        
        user = update.effective_user
        db.update_user_activity(user.id)
        
        from bot import bot
        
        info_text = f"""
ℹ️ <b>Informasi Bot</b>

🤖 <b>Nama:</b> {BOT_NAME}
📌 <b>Versi:</b> <code>{BOT_VERSION}</code>
👤 <b>Author:</b> <code>{BOT_AUTHOR}</code>
⏱️ <b>Uptime:</b> {self.get_uptime()}

📦 <b>Plugin terinstall:</b> {bot.plugin_manager.plugin_count}
👥 <b>Total pengguna:</b> {db.get_user_count()}

<i>Bot modular yang mudah dikembangkan!</i>
"""
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Statistik", callback_data="menu_stats")],
            [InlineKeyboardButton(BUTTON_BACK, callback_data="menu_main")]
        ])
        
        await query.edit_message_text(info_text, parse_mode="HTML", reply_markup=keyboard)
    
    async def cb_menu_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk callback menu_stats"""
        query = update.callback_query
        await query.answer("🔄 Data diperbarui!")
        
        user = update.effective_user
        db.update_user_activity(user.id)
        
        await self._show_stats(update, context, is_callback=True)

# Instance plugin
plugin = InfoPlugin()
