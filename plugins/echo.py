"""
========================================
Plugin: Echo
========================================
Nama: Echo
Deskripsi: Plugin untuk mengulang pesan yang dikirim user
Commands:
  - /echo [teks]: Mengulang teks yang dikirim
  - /upper [teks]: Mengubah teks menjadi huruf besar
  - /lower [teks]: Mengubah teks menjadi huruf kecil
  - /reverse [teks]: Membalik teks
Contoh Penggunaan:
  - /echo Halo dunia!
  - /upper hello world
  - /lower HALLO
  - /reverse Hello
========================================
"""

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger

class EchoPlugin(PluginBase):
    """Plugin untuk echo dan manipulasi teks"""
    
    PLUGIN_NAME = "Echo"
    PLUGIN_DESCRIPTION = "Mengulang dan memanipulasi teks"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "utility"
    
    COMMANDS = [
        {"command": "echo", "description": "Mengulang teks", "handler": "cmd_echo"},
        {"command": "upper", "description": "Ubah teks jadi huruf besar", "handler": "cmd_upper"},
        {"command": "lower", "description": "Ubah teks jadi huruf kecil", "handler": "cmd_lower"},
        {"command": "reverse", "description": "Membalik teks", "handler": "cmd_reverse"}
    ]
    
    EXAMPLES = [
        "/echo Halo dunia!",
        "/upper hello world",
        "/lower HALLO",
        "/reverse Hello World"
    ]
    
    async def initialize(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    async def cmd_echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /echo
        Format: /echo [teks]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/echo [teks]</code>\n\n"
                "<i>Contoh: /echo Halo dunia!</i>",
                parse_mode="HTML"
            )
            return
        
        logger.command_used("/echo", user.id, user.username)
        
        text = " ".join(context.args)
        await update.message.reply_text(f"📢 <b>Echo:</b>\n{text}", parse_mode="HTML")
    
    async def cmd_upper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /upper
        Format: /upper [teks]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/upper [teks]</code>\n\n"
                "<i>Contoh: /upper hello world</i>",
                parse_mode="HTML"
            )
            return
        
        logger.command_used("/upper", user.id, user.username)
        
        text = " ".join(context.args)
        await update.message.reply_text(
            f"🔠 <b>Uppercase:</b>\n<code>{text.upper()}</code>",
            parse_mode="HTML"
        )
    
    async def cmd_lower(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /lower
        Format: /lower [teks]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/lower [teks]</code>\n\n"
                "<i>Contoh: /lower HALLO</i>",
                parse_mode="HTML"
            )
            return
        
        logger.command_used("/lower", user.id, user.username)
        
        text = " ".join(context.args)
        await update.message.reply_text(
            f"🔡 <b>Lowercase:</b>\n<code>{text.lower()}</code>",
            parse_mode="HTML"
        )
    
    async def cmd_reverse(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /reverse
        Format: /reverse [teks]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/reverse [teks]</code>\n\n"
                "<i>Contoh: /reverse Hello</i>",
                parse_mode="HTML"
            )
            return
        
        logger.command_used("/reverse", user.id, user.username)
        
        text = " ".join(context.args)
        reversed_text = text[::-1]
        
        await update.message.reply_text(
            f"🔄 <b>Reverse:</b>\n"
            f"<b>Original:</b> <code>{text}</code>\n"
            f"<b>Reversed:</b> <code>{reversed_text}</code>",
            parse_mode="HTML"
        )

# Instance plugin
plugin = EchoPlugin()
