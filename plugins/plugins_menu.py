"""
========================================
Plugin: Plugins Menu
========================================
Nama: Plugins Menu
Deskripsi: Plugin untuk menampilkan daftar plugin dengan pagination
Commands:
  - /plugins: Menampilkan daftar plugin
Contoh Penggunaan:
  - /plugins
  - Klik tombol "📦 Plugins" di menu utama
  - Klik "◀️ Prev" atau "▶️ Next" untuk navigasi
========================================
"""

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from core.plugin_base import PluginBase
from config import PLUGINS_PER_PAGE, BUTTON_BACK, EMOJI_PLUGINS
from utils.database import db
from utils.logger import logger

class PluginsMenuPlugin(PluginBase):
    """Plugin untuk menampilkan daftar plugin dengan pagination"""
    
    PLUGIN_NAME = "Plugins Menu"
    PLUGIN_DESCRIPTION = "Menampilkan daftar plugin dengan sistem pagination"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "info"
    
    # Path ke gambar banner
    BANNER_PATH = "media/banner.jpg"
    
    COMMANDS = [
        {"command": "plugins", "description": "Menampilkan daftar plugin", "handler": "cmd_plugins"}
    ]
    
    EXAMPLES = [
        "/plugins",
        "Klik 📦 Plugins di menu utama"
    ]
    
    def __init__(self):
        super().__init__()
        # Register callback handlers untuk pagination
        self.add_handler(CallbackQueryHandler(self.cb_plugins_list, pattern="^plugins_list_"))
        self.add_handler(CallbackQueryHandler(self.cb_plugin_detail, pattern="^plugin_detail_"))
    
    async def initialize(self):
        """Inisialisasi plugin"""
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        """Shutdown plugin"""
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    def get_category_emoji(self, category: str) -> str:
        """Mendapatkan emoji berdasarkan kategori"""
        return EMOJI_PLUGINS.get(category, "📦")
    
    def create_plugins_keyboard(self, plugins: list, page: int, total_pages: int) -> InlineKeyboardMarkup:
        """Membuat keyboard untuk daftar plugin dengan pagination"""
        keyboard = []
        
        # Tombol untuk setiap plugin
        for plugin_info in plugins:
            emoji = self.get_category_emoji(plugin_info["category"])
            btn_text = f"{emoji} {plugin_info['name']}"
            callback_data = f"plugin_detail_{plugin_info['name']}"
            keyboard.append([InlineKeyboardButton(btn_text, callback_data=callback_data)])
        
        # Tombol pagination
        if total_pages > 1:
            pagination_row = []
            if page > 0:
                pagination_row.append(InlineKeyboardButton("◀️ Prev", callback_data=f"plugins_list_{page - 1}"))
            else:
                pagination_row.append(InlineKeyboardButton("⏹️", callback_data="noop"))
            
            pagination_row.append(InlineKeyboardButton(f"{page + 1} / {total_pages}", callback_data="noop"))
            
            if page < total_pages - 1:
                pagination_row.append(InlineKeyboardButton("▶️ Next", callback_data=f"plugins_list_{page + 1}"))
            else:
                pagination_row.append(InlineKeyboardButton("⏹️", callback_data="noop"))
            
            keyboard.append(pagination_row)
        
        keyboard.append([InlineKeyboardButton(BUTTON_BACK, callback_data="menu_main")])
        return InlineKeyboardMarkup(keyboard)
    
    def create_plugin_detail_keyboard(self, plugin_name: str) -> InlineKeyboardMarkup:
        """Membuat keyboard untuk detail plugin"""
        keyboard = [[InlineKeyboardButton(BUTTON_BACK, callback_data="plugins_list_0")]]
        return InlineKeyboardMarkup(keyboard)
    
    async def cmd_plugins(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk command /plugins"""
        user = update.effective_user
        db.update_user_activity(user.id)
        logger.command_used("/plugins", user.id, user.username)
        await self._show_plugins_list(update, context, page=0, is_callback=False)
    
    async def cb_plugins_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk callback pagination"""
        query = update.callback_query
        await query.answer()
        
        try:
            page = int(query.data.split("_")[-1])
        except (ValueError, IndexError):
            page = 0
        
        await self._show_plugins_list(update, context, page=page, is_callback=True)
    
    async def _show_plugins_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                page: int, is_callback: bool = False):
        """Helper untuk menampilkan daftar plugin (Media-Aware)"""
        from bot import bot
        all_plugins = bot.plugin_manager.get_all_plugin_info()
        total_plugins = len(all_plugins)
        
        if total_plugins == 0:
            text = "📦 <b>Daftar Plugin</b>\n\n<i>Belum ada plugin yang terinstall.</i>"
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(BUTTON_BACK, callback_data="menu_main")]])
        else:
            total_pages = (total_plugins + PLUGINS_PER_PAGE - 1) // PLUGINS_PER_PAGE
            page = max(0, min(page, total_pages - 1))
            start_idx = page * PLUGINS_PER_PAGE
            page_plugins = all_plugins[start_idx : start_idx + PLUGINS_PER_PAGE]
            
            text = (f"📦 <b>Daftar Plugin</b>\n\n"
                    f"<i>Total: {total_plugins} plugin | Halaman {page + 1}/{total_pages}</i>\n\n"
                    f"<i>Klik plugin untuk melihat detailnya:</i>")
            keyboard = self.create_plugins_keyboard(page_plugins, page, total_pages)

        # Logika Pengiriman Gambar
        banner_exists = os.path.exists(self.BANNER_PATH)
        
        if is_callback:
            query = update.callback_query
            if banner_exists:
                with open(self.BANNER_PATH, 'rb') as photo:
                    if query.message.photo:
                        # Jika pesan sudah ada foto, edit media & caption
                        await query.edit_message_media(
                            media=InputMediaPhoto(media=photo, caption=text, parse_mode="HTML"),
                            reply_markup=keyboard
                        )
                    else:
                        # Jika pesan sebelumnya teks, hapus dan kirim pesan foto baru
                        await query.message.delete()
                        await context.bot.send_photo(
                            chat_id=update.effective_chat.id,
                            photo=photo,
                            caption=text,
                            parse_mode="HTML",
                            reply_markup=keyboard
                        )
            else:
                # Fallback: Jika gambar tidak ada, edit teks saja (atau delete jika sebelumnya foto)
                if query.message.photo:
                    await query.message.delete()
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=text,
                        parse_mode="HTML",
                        reply_markup=keyboard
                    )
                else:
                    await query.edit_message_text(text, parse_mode="HTML", reply_markup=keyboard)
        else:
            # Command /plugins
            if banner_exists:
                with open(self.BANNER_PATH, 'rb') as photo:
                    await update.message.reply_photo(photo=photo, caption=text, parse_mode="HTML", reply_markup=keyboard)
            else:
                await update.message.reply_text(text, parse_mode="HTML", reply_markup=keyboard)

    async def cb_plugin_detail(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk detail plugin (Media-Aware)"""
        query = update.callback_query
        await query.answer()
        
        plugin_name = query.data.replace("plugin_detail_", "")
        from bot import bot
        plugin = bot.plugin_manager.get_plugin(plugin_name)
        
        if not plugin:
            text = f"⚠️ Plugin <b>{plugin_name}</b> tidak ditemukan!"
            kb = InlineKeyboardMarkup([[InlineKeyboardButton(BUTTON_BACK, callback_data="plugins_list_0")]])
        else:
            db.update_plugin_usage(plugin_name)
            text = plugin.get_info_text()
            kb = self.create_plugin_detail_keyboard(plugin_name)
        
        # Cek tipe pesan agar tidak error "no text in message"
        if query.message.photo:
            await query.edit_message_caption(caption=text, parse_mode="HTML", reply_markup=kb)
        else:
            await query.edit_message_text(text, parse_mode="HTML", reply_markup=kb)

# Instance plugin
plugin = PluginsMenuPlugin()