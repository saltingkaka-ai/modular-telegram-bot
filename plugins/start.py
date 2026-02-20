"""
========================================
Plugin: Start
========================================
Nama: Start
Deskripsi: Plugin untuk menangani command /start dan menu utama
Commands:
  - /start: Memulai bot dan menampilkan menu utama
  - /menu: Menampilkan menu utama
Contoh Penggunaan:
  - /start
  - /menu
  - Klik tombol "🔙 Kembali" di menu lain
========================================
"""

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from core.plugin_base import PluginBase
from config import (
    BOT_NAME, BOT_VERSION, WELCOME_MESSAGE, 
    BUTTON_PLUGINS, BUTTON_HELP, BUTTON_INFO, BUTTON_BACK
)
from utils.database import db
from utils.logger import logger

class StartPlugin(PluginBase):
    """Plugin untuk menu utama dan start command"""
    
    PLUGIN_NAME = "Start"
    PLUGIN_DESCRIPTION = "Menu utama dan welcome message"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "info"
    
    BANNER_PATH = "media/banner.jpg" # Lokasi gambar banner
    
    COMMANDS = [
        {"command": "start", "description": "Memulai bot", "handler": "cmd_start"},
        {"command": "menu", "description": "Menampilkan menu utama", "handler": "cmd_menu"}
    ]
    
    EXAMPLES = [
        "/start",
        "/menu"
    ]
    
    def __init__(self):
        super().__init__()
        # Tambahkan callback query handler untuk menu
        self.add_handler(CallbackQueryHandler(self.cb_menu_main, pattern="^menu_main$"))
    
    async def initialize(self):
        """Inisialisasi plugin"""
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        """Shutdown plugin"""
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    def get_main_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Membuat keyboard menu utama"""
        keyboard = [
            [
                InlineKeyboardButton(BUTTON_PLUGINS, callback_data="plugins_list_0"),
                InlineKeyboardButton(BUTTON_HELP, callback_data="menu_help")
            ],
            [
                InlineKeyboardButton(BUTTON_INFO, callback_data="menu_info"),
                InlineKeyboardButton("📊 Statistik", callback_data="menu_stats")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    async def _show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, is_callback: bool = False):
        """Helper internal untuk menampilkan menu dengan gambar atau teks"""
        keyboard = self.get_main_menu_keyboard()

        if os.path.exists(self.BANNER_PATH):
            with open(self.BANNER_PATH, 'rb') as photo:
                if is_callback:
                    query = update.callback_query
                    # Jika pesan saat ini sudah punya foto, edit medianya
                    if query.message.photo:
                        await query.edit_message_media(
                            media=InputMediaPhoto(media=photo, caption=text, parse_mode="HTML"),
                            reply_markup=keyboard
                        )
                    else:
                        # Jika sebelumnya pesan teks, hapus dan kirim pesan foto baru
                        await query.message.delete()
                        await context.bot.send_photo(
                            chat_id=update.effective_chat.id,
                            photo=photo,
                            caption=text,
                            parse_mode="HTML",
                            reply_markup=keyboard
                        )
                else:
                    # Untuk command /start atau /menu
                    await update.effective_message.reply_photo(
                        photo=photo,
                        caption=text,
                        parse_mode="HTML",
                        reply_markup=keyboard
                    )
        else:
            # Fallback jika gambar banner tidak ditemukan
            if is_callback:
                await update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=keyboard)
            else:
                await update.effective_message.reply_text(text, parse_mode="HTML", reply_markup=keyboard)
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /start
        Menampilkan welcome message dan menu utama
        """
        user = update.effective_user
        
        # Simpan/update user ke database
        db.add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            language_code=user.language_code,
            is_bot=user.is_bot
        )
        
        db.update_user_activity(user.id)
        logger.command_used("/start", user.id, user.username)
        
        from bot import bot
        plugin_count = bot.plugin_manager.plugin_count
        
        welcome_text = WELCOME_MESSAGE.format(
            bot_name=BOT_NAME,
            version=BOT_VERSION,
            plugin_count=plugin_count
        )
        
        await self._show_main_menu(update, context, welcome_text, is_callback=False)
    
    async def cmd_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /menu
        Menampilkan menu utama
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        logger.command_used("/menu", user.id, user.username)
        
        from bot import bot
        plugin_count = bot.plugin_manager.plugin_count
        
        menu_text = f"""
📋 <b>Menu Utama</b>

🤖 <b>{BOT_NAME}</b> v{BOT_VERSION}
📦 <b>Plugin terinstall:</b> {plugin_count}

<i>Pilih menu di bawah ini:</i>
"""
        await self._show_main_menu(update, context, menu_text, is_callback=False)
    
    async def cb_menu_main(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk callback menu_main
        Kembali ke menu utama
        """
        query = update.callback_query
        await query.answer()
        
        user = update.effective_user
        db.update_user_activity(user.id)
        
        from bot import bot
        plugin_count = bot.plugin_manager.plugin_count
        
        menu_text = f"""
📋 <b>Menu Utama</b>

🤖 <b>{BOT_NAME}</b> v{BOT_VERSION}
📦 <b>Plugin terinstall:</b> {plugin_count}

<i>Pilih menu di bawah ini:</i>
"""
        await self._show_main_menu(update, context, menu_text, is_callback=True)

# Instance plugin
plugin = StartPlugin()