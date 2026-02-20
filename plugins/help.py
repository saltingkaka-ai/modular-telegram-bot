"""
========================================
Plugin: Help
========================================
Nama: Help
Deskripsi: Plugin untuk menampilkan bantuan dan panduan penggunaan
Commands:
  - /help: Menampilkan pesan bantuan
  - /help [plugin]: Menampilkan bantuan untuk plugin tertentu
Contoh Penggunaan:
  - /help
  - /help start
  - /help plugins
========================================
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from core.plugin_base import PluginBase
from config import BUTTON_BACK, HELP_MESSAGE
from utils.database import db
from utils.logger import logger

class HelpPlugin(PluginBase):
    """Plugin untuk bantuan dan panduan"""
    
    PLUGIN_NAME = "Help"
    PLUGIN_DESCRIPTION = "Sistem bantuan dan panduan penggunaan"
    PLUGIN_VERSION = "1.1"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "info"
    
    COMMANDS = [
        {"command": "help", "description": "Menampilkan bantuan", "handler": "cmd_help"}
    ]
    
    EXAMPLES = [
        "/help",
        "/help start",
        "/help plugins"
    ]
    
    def __init__(self):
        super().__init__()
        self.add_handler(CallbackQueryHandler(self.cb_menu_help, pattern="^menu_help$"))
    
    async def initialize(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /help
        Format: /help atau /help [plugin_name]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        args = context.args
        
        if args:
            # Bantuan untuk plugin tertentu
            plugin_name = args[0].lower()
            await self._show_plugin_help(update, context, plugin_name)
        else:
            # Bantuan umum
            logger.command_used("/help", user.id, user.username)
            await self._show_general_help(update, context, is_callback=False)
    
    async def _show_general_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool = False):
        """
        Menampilkan bantuan umum
        Args:
            is_callback: True jika dipanggil dari callback query, False jika dari command
        """
        from bot import bot
        
        # Kumpulkan semua commands dari semua plugin
        all_commands = []
        for plugin_info in bot.plugin_manager.get_all_plugin_info():
            for cmd in plugin_info.get("commands", []):
                all_commands.append({
                    "command": cmd["command"],
                    "description": cmd.get("description", "No description"),
                    "plugin": plugin_info["name"]
                })
        
        # Sort commands
        all_commands.sort(key=lambda x: x["command"])
        
        # Buat teks bantuan
        help_text = "📖 <b>Daftar Command Tersedia</b>\n\n"
        
        for cmd in all_commands:
            help_text += f"  /{cmd['command']} - {cmd['description']}\n"
        
        help_text += f"\n<i>Gunakan /help [nama_plugin] untuk detail plugin tertentu</i>"
        help_text += f"\n<i>Contoh: /help start</i>"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(BUTTON_BACK, callback_data="menu_main")]
        ])
        
        if is_callback:
            query = update.callback_query
            # FIX: Cek apakah pesan memiliki foto atau teks
            if query.message.photo:
                # Jika pesan berisi foto, hapus dan kirim pesan teks baru
                await query.message.delete()
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=help_text,
                    parse_mode="HTML",
                    reply_markup=keyboard
                )
            else:
                # Jika pesan teks, edit saja
                await query.edit_message_text(help_text, parse_mode="HTML", reply_markup=keyboard)
        else:
            # Dari command /help
            await update.message.reply_text(help_text, parse_mode="HTML", reply_markup=keyboard)
    
    async def _show_plugin_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE, plugin_name: str):
        """Menampilkan bantuan untuk plugin tertentu"""
        from bot import bot
        
        # Cari plugin
        plugin = bot.plugin_manager.get_plugin(plugin_name)
        
        if not plugin:
            await update.message.reply_text(
                f"⚠️ Plugin <b>{plugin_name}</b> tidak ditemukan!\n\n"
                f"Gunakan /plugins untuk melihat daftar plugin yang tersedia.",
                parse_mode="HTML"
            )
            return
        
        logger.command_used(f"/help {plugin_name}", update.effective_user.id, update.effective_user.username)
        
        # Tampilkan info plugin
        help_text = plugin.get_info_text()
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📦 Lihat Semua Plugin", callback_data="plugins_list_0")],
            [InlineKeyboardButton(BUTTON_BACK, callback_data="menu_main")]
        ])
        
        await update.message.reply_text(help_text, parse_mode="HTML", reply_markup=keyboard)
    
    async def cb_menu_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk callback menu_help"""
        query = update.callback_query
        await query.answer()
        
        user = update.effective_user
        db.update_user_activity(user.id)
        
        # Panggil _show_general_help dengan is_callback=True
        await self._show_general_help(update, context, is_callback=True)

# Instance plugin
plugin = HelpPlugin()