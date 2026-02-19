"""
========================================
Modular Telegram Bot - Logger
========================================
Nama: Logger
Deskripsi: Sistem logging untuk bot
Command: -
Usage: Import dari file lain
========================================
"""

import logging
import os
import sys
from datetime import datetime
from typing import Optional

class ColoredFormatter(logging.Formatter):
    """Formatter dengan warna untuk terminal"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset_color = self.COLORS['RESET']
        
        # Format dengan warna
        formatted = f"{log_color}[{record.levelname}]{reset_color} {record.getMessage()}"
        return formatted

class BotLogger:
    """Logger khusus untuk bot"""
    
    def __init__(self, name: str = "ModularBot", log_level: str = "INFO", 
                 log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        self.logger.handlers = []  # Clear existing handlers
        
        # Console Handler dengan warna
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = ColoredFormatter()
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File Handler
        if log_file:
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Log level DEBUG"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log level INFO"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log level WARNING"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log level ERROR"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log level CRITICAL"""
        self.logger.critical(message)
    
    def plugin_loaded(self, plugin_name: str):
        """Log saat plugin diload"""
        self.info(f"📦 Plugin loaded: {plugin_name}")
    
    def plugin_error(self, plugin_name: str, error: str):
        """Log error plugin"""
        self.error(f"❌ Plugin error [{plugin_name}]: {error}")
    
    def command_used(self, command: str, user_id: int, username: Optional[str] = None):
        """Log penggunaan command"""
        user_info = f"@{username}" if username else f"ID:{user_id}"
        self.debug(f"⌨️  Command '{command}' used by {user_info}")
    
    def bot_started(self, version: str, plugin_count: int):
        """Log saat bot dimulai"""
        self.info(f"🚀 Bot started! Version: {version} | Plugins: {plugin_count}")
    
    def bot_stopped(self):
        """Log saat bot dihentikan"""
        self.info("🛑 Bot stopped!")

# Singleton instance
logger = BotLogger()
