"""
========================================
Modular Telegram Bot - Plugin Base
========================================
Nama: PluginBase
Deskripsi: Base class untuk semua plugin
Command: -
Usage: Extend class ini untuk membuat plugin baru
========================================
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler

@dataclass
class PluginInfo:
    """Data class untuk informasi plugin"""
    name: str
    description: str = "No description"
    version: str = "1.0"
    author: str = "Unknown"
    category: str = "other"  # admin, fun, utility, info, media, other
    commands: List[Dict[str, str]] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ke dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "category": self.category,
            "commands": self.commands,
            "examples": self.examples,
            "is_active": self.is_active
        }

class PluginBase(ABC):
    """
    Base class untuk semua plugin.
    
    Setiap plugin harus meng-extend class ini dan mengimplementasikan
    method-method yang diperlukan.
    """
    
    # Plugin metadata - WAJIB diisi oleh subclass
    PLUGIN_NAME: str = "BasePlugin"
    PLUGIN_DESCRIPTION: str = "Base plugin description"
    PLUGIN_VERSION: str = "1.0"
    PLUGIN_AUTHOR: str = "Unknown"
    PLUGIN_CATEGORY: str = "other"
    
    # Commands yang disediakan plugin
    # Format: [{"command": "start", "description": "Start the bot", "handler": "cmd_start"}]
    COMMANDS: List[Dict[str, str]] = []
    
    # Contoh penggunaan
    EXAMPLES: List[str] = []
    
    def __init__(self):
        self.info = PluginInfo(
            name=self.PLUGIN_NAME,
            description=self.PLUGIN_DESCRIPTION,
            version=self.PLUGIN_VERSION,
            author=self.PLUGIN_AUTHOR,
            category=self.PLUGIN_CATEGORY,
            commands=self.COMMANDS,
            examples=self.EXAMPLES
        )
        self._handlers = []
        self._is_loaded = False
    
    @property
    def name(self) -> str:
        """Nama plugin"""
        return self.PLUGIN_NAME
    
    @property
    def description(self) -> str:
        """Deskripsi plugin"""
        return self.PLUGIN_DESCRIPTION
    
    @property
    def version(self) -> str:
        """Versi plugin"""
        return self.PLUGIN_VERSION
    
    @property
    def is_loaded(self) -> bool:
        """Status load plugin"""
        return self._is_loaded
    
    def get_handlers(self) -> List:
        """
        Mendapatkan semua handlers untuk plugin ini.
        Override method ini jika perlu custom handlers.
        """
        handlers = []
        
        # Register command handlers dari COMMANDS
        for cmd_info in self.COMMANDS:
            command = cmd_info.get("command")
            handler_name = cmd_info.get("handler", f"cmd_{command}")
            
            if hasattr(self, handler_name):
                handler_method = getattr(self, handler_name)
                handlers.append(CommandHandler(command, handler_method))
        
        # Register custom handlers jika ada
        handlers.extend(self._handlers)
        
        return handlers
    
    def add_handler(self, handler):
        """Menambahkan custom handler"""
        self._handlers.append(handler)
    
    @abstractmethod
    async def initialize(self):
        """
        Method yang dipanggil saat plugin diinisialisasi.
        Override ini untuk setup awal plugin.
        """
        pass
    
    @abstractmethod
    async def shutdown(self):
        """
        Method yang dipanggil saat plugin dimatikan.
        Override ini untuk cleanup.
        """
        pass
    
    # Helper methods
    def get_info_text(self) -> str:
        """Mendapatkan teks informasi plugin"""
        emoji_map = {
            "admin": "👮",
            "fun": "🎮",
            "utility": "🛠️",
            "info": "📊",
            "media": "🎵",
            "other": "📦"
        }
        emoji = emoji_map.get(self.PLUGIN_CATEGORY, "📦")
        
        text = f"""
{emoji} <b>{self.PLUGIN_NAME}</b>

📝 <b>Deskripsi:</b>
<i>{self.PLUGIN_DESCRIPTION}</i>

📌 <b>Versi:</b> <code>{self.PLUGIN_VERSION}</code>
👤 <b>Author:</b> <code>{self.PLUGIN_AUTHOR}</code>
🏷️ <b>Kategori:</b> <code>{self.PLUGIN_CATEGORY}</code>
"""
        
        if self.COMMANDS:
            text += "\n⌨️ <b>Commands:</b>\n"
            for cmd in self.COMMANDS:
                text += f"  • /{cmd['command']} - {cmd.get('description', 'No description')}\n"
        
        if self.EXAMPLES:
            text += "\n📖 <b>Contoh Penggunaan:</b>\n"
            for example in self.EXAMPLES:
                text += f"  <code>{example}</code>\n"
        
        return text
    
    def create_back_button(self, callback_data: str = "menu_main") -> InlineKeyboardButton:
        """Membuat tombol kembali"""
        return InlineKeyboardButton("🔙 Kembali", callback_data=callback_data)
    
    def create_close_button(self) -> InlineKeyboardButton:
        """Membuat tombol tutup"""
        return InlineKeyboardButton("❌ Tutup", callback_data="menu_close")
    
    async def answer_callback(self, update: Update, text: Optional[str] = None, 
                            show_alert: bool = False):
        """Helper untuk answer callback query"""
        if update.callback_query:
            await update.callback_query.answer(text=text, show_alert=show_alert)
