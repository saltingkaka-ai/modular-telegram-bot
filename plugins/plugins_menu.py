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

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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
        """
        Membuat keyboard untuk daftar plugin dengan pagination
        
        Args:
            plugins: List plugin untuk halaman ini
            page: Halaman saat ini (0-indexed)
            total_pages: Total halaman
        
        Returns:
            InlineKeyboardMarkup
        """
        keyboard = []
        
        # Tombol untuk setiap plugin
        for plugin_info in plugins:
            emoji = self.get_category_emoji(plugin_info["category"])
            btn_text = f"{emoji} {plugin_info['name']}"
            callback_data = f"plugin_detail_{plugin_info['name']}"
            keyboard.append([InlineKeyboardButton(btn_text, callback_data=callback_data)])
        
        # Tombol pagination (hanya ditampilkan jika ada lebih dari 1 halaman)
        if total_pages > 1:
            pagination_row = []
            
            # Tombol Prev (disabled jika di halaman pertama)
            if page > 0:
                pagination_row.append(
                    InlineKeyboardButton("◀️ Prev", callback_data=f"plugins_list_{page - 1}")
                )
            else:
                pagination_row.append(
                    InlineKeyboardButton("⏹️", callback_data="noop")
                )
            
            # Tombol halaman (tidak bisa diklik)
            pagination_row.append(
                InlineKeyboardButton(f"{page + 1} / {total_pages}", callback_data="noop")
            )
            
            # Tombol Next (disabled jika di halaman terakhir)
            if page < total_pages - 1:
                pagination_row.append(
                    InlineKeyboardButton("▶️ Next", callback_data=f"plugins_list_{page + 1}")
                )
            else:
                pagination_row.append(
                    InlineKeyboardButton("⏹️", callback_data="noop")
                )
            
            keyboard.append(pagination_row)
        
        # Tombol kembali (WAJIB ADA)
        keyboard.append([InlineKeyboardButton(BUTTON_BACK, callback_data="menu_main")])
        
        return InlineKeyboardMarkup(keyboard)
    
    def create_plugin_detail_keyboard(self, plugin_name: str) -> InlineKeyboardMarkup:
        """Membuat keyboard untuk detail plugin"""
        keyboard = [
            [InlineKeyboardButton(BUTTON_BACK, callback_data="plugins_list_0")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    async def cmd_plugins(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /plugins
        Menampilkan daftar plugin dengan pagination
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        logger.command_used("/plugins", user.id, user.username)
        
        await self._show_plugins_list(update, context, page=0, is_callback=False)
    
    async def cb_plugins_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk callback plugins_list_{page}
        Menampilkan daftar plugin dengan pagination
        """
        query = update.callback_query
        await query.answer()
        
        user = update.effective_user
        db.update_user_activity(user.id)
        
        # Extract page number dari callback data
        callback_data = query.data
        try:
            page = int(callback_data.split("_")[-1])
        except ValueError:
            page = 0
        
        await self._show_plugins_list(update, context, page=page, is_callback=True)
    
    async def _show_plugins_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                page: int, is_callback: bool = False):
        """
        Helper method untuk menampilkan daftar plugin
        
        Args:
            update: Update object
            context: Context object
            page: Halaman yang akan ditampilkan (0-indexed)
            is_callback: True jika dipanggil dari callback, False jika dari command
        """
        from bot import bot
        
        # Dapatkan semua plugin info
        all_plugins = bot.plugin_manager.get_all_plugin_info()
        total_plugins = len(all_plugins)
        
        if total_plugins == 0:
            text = """
📦 <b>Daftar Plugin</b>

<i>Belum ada plugin yang terinstall.</i>
"""
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(BUTTON_BACK, callback_data="menu_main")]])
            
            if is_callback:
                await update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=keyboard)
            else:
                await update.message.reply_text(text, parse_mode="HTML", reply_markup=keyboard)
            return
        
        # Hitung pagination
        total_pages = (total_plugins + PLUGINS_PER_PAGE - 1) // PLUGINS_PER_PAGE
        
        # Validasi page
        page = max(0, min(page, total_pages - 1))
        
        # Ambil plugin untuk halaman ini
        start_idx = page * PLUGINS_PER_PAGE
        end_idx = start_idx + PLUGINS_PER_PAGE
        page_plugins = all_plugins[start_idx:end_idx]
        
        # Buat teks
        text = f"""
📦 <b>Daftar Plugin</b>

<i>Total: {total_plugins} plugin | Halaman {page + 1}/{total_pages}</i>

<i>Klik plugin untuk melihat detailnya:</i>
"""
        
        # Buat keyboard
        keyboard = self.create_plugins_keyboard(page_plugins, page, total_pages)
        
        # Kirim/edit pesan
        if is_callback:
            await update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=keyboard)
        else:
            await update.message.reply_text(text, parse_mode="HTML", reply_markup=keyboard)
    
    async def cb_plugin_detail(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk callback plugin_detail_{name}
        Menampilkan detail plugin
        """
        query = update.callback_query
        await query.answer()
        
        user = update.effective_user
        db.update_user_activity(user.id)
        
        # Extract plugin name dari callback data
        callback_data = query.data
        plugin_name = callback_data.replace("plugin_detail_", "")
        
        from bot import bot
        plugin = bot.plugin_manager.get_plugin(plugin_name)
        
        if not plugin:
            await query.edit_message_text(
                f"⚠️ Plugin <b>{plugin_name}</b> tidak ditemukan!",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(BUTTON_BACK, callback_data="plugins_list_0")]])
            )
            return
        
        # Update penggunaan plugin di database
        db.update_plugin_usage(plugin_name)
        
        # Tampilkan detail plugin
        detail_text = plugin.get_info_text()
        keyboard = self.create_plugin_detail_keyboard(plugin_name)
        
        await query.edit_message_text(detail_text, parse_mode="HTML", reply_markup=keyboard)

# Instance plugin
plugin = PluginsMenuPlugin()
