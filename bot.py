"""
========================================
Modular Telegram Bot - Main Bot
========================================
Nama: ModularBot
Deskripsi: File utama bot yang mengelola aplikasi
Command: -
Usage: Jalankan file ini untuk memulai bot
========================================
"""

import asyncio
import signal
import sys
from typing import Optional

from telegram import Update, Bot
from telegram.ext import (
    Application,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from config import (
    BOT_TOKEN, BOT_NAME, BOT_VERSION, BOT_AUTHOR,
    LOG_LEVEL, LOG_FILE, PLUGINS_FOLDER,
    WELCOME_MESSAGE, HELP_MESSAGE,
    BUTTON_PLUGINS, BUTTON_HELP, BUTTON_INFO, BUTTON_BACK
)
from core.plugin_manager import PluginManager
from utils.logger import BotLogger, logger
from utils.database import db

class ModularBot:
    """
    Class utama untuk bot modular.
    Mengelola aplikasi, plugin manager, dan lifecycle bot.
    """
    
    def __init__(self):
        self.application: Optional[Application] = None
        self.plugin_manager = PluginManager(PLUGINS_FOLDER)
        self.logger = BotLogger("ModularBot", LOG_LEVEL, LOG_FILE)
        self._running = False
        
        # Validasi token
        if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            self.logger.error("❌ BOT_TOKEN belum diatur! Silakan edit config.py atau set environment variable.")
            sys.exit(1)
    
    async def initialize(self):
        """Inisialisasi bot dan semua komponen"""
        self.logger.info("🔄 Initializing bot...")
        
        # Buat application
        self.application = (
            ApplicationBuilder()
            .token(BOT_TOKEN)
            .build()
        )
        
        # Load semua plugin
        self.plugin_manager.load_all_plugins()
        
        # Register handlers dari plugin
        handlers = self.plugin_manager.get_handlers_for_application()
        for handler in handlers:
            self.application.add_handler(handler)
        
        # Register error handler
        self.application.add_error_handler(self._error_handler)
        
        # Inisialisasi semua plugin
        await self.plugin_manager.initialize_all_plugins()
        
        # Setup signal handlers untuk graceful shutdown
        for sig in (signal.SIGINT, signal.SIGTERM):
            asyncio.get_event_loop().add_signal_handler(
                sig, lambda: asyncio.create_task(self.shutdown())
            )
        
        self._running = True
        self.logger.bot_started(BOT_VERSION, self.plugin_manager.plugin_count)
    
    async def run(self):
        """Menjalankan bot"""
        await self.initialize()
        
        self.logger.info("🚀 Starting bot polling...")
        
        # Start the bot
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling(drop_pending_updates=True)
        
        # Keep running sampai dihentikan
        while self._running:
            await asyncio.sleep(1)
        
        # Cleanup
        await self.shutdown()
    
    async def shutdown(self):
        """Shutdown bot dengan graceful"""
        if not self._running:
            return
        
        self._running = False
        self.logger.info("🛑 Shutting down bot...")
        
        # Shutdown semua plugin
        await self.plugin_manager.shutdown_all_plugins()
        
        # Stop application
        if self.application:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
        
        self.logger.bot_stopped()
    
    async def _error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler untuk error"""
        self.logger.error(f"Exception while handling update: {context.error}")
        
        # Log detail error
        import traceback
        self.logger.error(traceback.format_exc())
        
        # Kirim pesan error ke user jika ada update
        if update and update.effective_message:
            try:
                await update.effective_message.reply_text(
                    "⚠️ <b>Terjadi kesalahan!</b>\n\n"
                    "Maaf, ada masalah saat memproses permintaan Anda.\n"
                    "Silakan coba lagi nanti.",
                    parse_mode="HTML"
                )
            except:
                pass
    
    # Helper methods untuk plugin
    def get_bot_info(self) -> dict:
        """Mendapatkan informasi bot"""
        return {
            "name": BOT_NAME,
            "version": BOT_VERSION,
            "author": BOT_AUTHOR,
            "plugin_count": self.plugin_manager.plugin_count,
            "plugins": self.plugin_manager.get_all_plugin_info()
        }
    
    async def send_broadcast(self, message: str, parse_mode: str = "HTML") -> dict:
        """
        Mengirim broadcast ke semua user.
        Hanya untuk admin.
        
        Returns:
            dict dengan hasil broadcast
        """
        from config import ADMIN_IDS
        
        users = db.get_all_users(limit=10000)
        success = 0
        failed = 0
        
        for user in users:
            try:
                await self.application.bot.send_message(
                    chat_id=user["user_id"],
                    text=message,
                    parse_mode=parse_mode
                )
                success += 1
            except Exception as e:
                failed += 1
                self.logger.error(f"Failed to send broadcast to {user['user_id']}: {e}")
        
        return {"success": success, "failed": failed, "total": len(users)}

# Singleton instance
bot = ModularBot()

# Entry point
if __name__ == "__main__":
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("\n👋 Bot dihentikan oleh user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
