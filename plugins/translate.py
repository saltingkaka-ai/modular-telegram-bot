"""
========================================
Plugin: Translate
========================================
Nama: Translate
Deskripsi: Plugin untuk menerjemahkan teks ke berbagai bahasa
Commands:
  - /translate [lang] [text]: Terjemahkan ke bahasa tertentu
  - /tr [lang] [text]: Shortcut untuk translate
  - /detect [text]: Deteksi bahasa teks
Contoh Penggunaan:
  - /translate en Halo dunia
  - /tr id Hello world
  - /detect Bonjour le monde
========================================
⚠️ OPTIONAL API KEY: GOOGLE_TRANSLATE_API_KEY
Without API key, will use free translation library (googletrans)
========================================
"""

import os
from telegram import Update
from telegram.ext import ContextTypes

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger

# Try to import googletrans (free library)
try:
    from googletrans import Translator, LANGUAGES
    HAS_TRANSLATOR = True
except ImportError:
    HAS_TRANSLATOR = False


class TranslatePlugin(PluginBase):
    """Plugin untuk terjemahan bahasa"""
    
    PLUGIN_NAME = "Translate"
    PLUGIN_DESCRIPTION = "Terjemahkan teks ke berbagai bahasa"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "utility"
    
    COMMANDS = [
        {"command": "translate", "description": "Terjemahkan teks", "handler": "cmd_translate"},
        {"command": "tr", "description": "Shortcut translate", "handler": "cmd_translate"},
        {"command": "detect", "description": "Deteksi bahasa", "handler": "cmd_detect"}
    ]
    
    EXAMPLES = [
        "/translate en Halo dunia",
        "/tr id Hello world",
        "/tr es Good morning",
        "/detect Bonjour le monde"
    ]
    
    # Popular language codes
    POPULAR_LANGS = {
        "id": "Indonesia",
        "en": "English",
        "es": "Español",
        "fr": "Français",
        "de": "Deutsch",
        "it": "Italiano",
        "pt": "Português",
        "ru": "Русский",
        "ja": "日本語",
        "ko": "한국어",
        "zh-cn": "中文 (简体)",
        "zh-tw": "中文 (繁體)",
        "ar": "العربية",
        "hi": "हिन्दी",
        "th": "ไทย",
        "vi": "Tiếng Việt",
        "nl": "Nederlands",
        "tr": "Türkçe"
    }
    
    def __init__(self):
        super().__init__()
        self.translator = None
        if HAS_TRANSLATOR:
            self.translator = Translator()
    
    async def initialize(self):
        if not HAS_TRANSLATOR:
            logger.warning(f"Plugin {self.PLUGIN_NAME}: googletrans library not installed!")
            logger.warning("Install with: pip install googletrans==4.0.0rc1")
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    def get_language_name(self, code: str) -> str:
        """Get language name from code"""
        if code in self.POPULAR_LANGS:
            return self.POPULAR_LANGS[code]
        if HAS_TRANSLATOR and code in LANGUAGES:
            return LANGUAGES[code].title()
        return code.upper()
    
    async def cmd_translate(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /translate dan /tr
        Format: /translate [lang_code] [text]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not HAS_TRANSLATOR:
            await update.message.reply_text(
                "❌ <b>Error:</b> Library terjemahan tidak terinstall!\n\n"
                "Install dengan:\n"
                "<code>pip install googletrans==4.0.0rc1</code>",
                parse_mode="HTML"
            )
            return
        
        if len(context.args) < 2:
            # Show help with popular languages
            help_text = (
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/translate [kode_bahasa] [teks]</code>\n"
                "<code>/tr [kode_bahasa] [teks]</code>\n\n"
                "<b>Bahasa populer:</b>\n"
            )
            
            for code, name in list(self.POPULAR_LANGS.items())[:10]:
                help_text += f"  • <code>{code}</code> - {name}\n"
            
            help_text += (
                f"\n<b>Contoh:</b>\n"
                f"<code>/tr en Halo dunia</code>\n"
                f"<code>/tr id Hello world</code>\n"
                f"<code>/tr es Good morning</code>"
            )
            
            await update.message.reply_text(help_text, parse_mode="HTML")
            return
        
        target_lang = context.args[0].lower()
        text = " ".join(context.args[1:])
        
        # Validasi panjang text
        if len(text) > 500:
            await update.message.reply_text(
                "❌ <b>Error:</b> Teks terlalu panjang! (maksimal 500 karakter)",
                parse_mode="HTML"
            )
            return
        
        logger.command_used(f"/translate {target_lang}", user.id, user.username)
        
        try:
            # Show loading
            status_msg = await update.message.reply_text(
                "⏳ <b>Menerjemahkan...</b>",
                parse_mode="HTML"
            )
            
            # Translate
            result = self.translator.translate(text, dest=target_lang)
            
            # Get language names
            src_lang_name = self.get_language_name(result.src)
            dest_lang_name = self.get_language_name(target_lang)
            
            response = (
                f"🌐 <b>Terjemahan</b>\n\n"
                f"<b>{src_lang_name} → {dest_lang_name}</b>\n\n"
                f"<b>Original:</b>\n<i>{text}</i>\n\n"
                f"<b>Translation:</b>\n<b>{result.text}</b>"
            )
            
            # Show pronunciation if available and different
            if hasattr(result, 'pronunciation') and result.pronunciation and result.pronunciation != result.text:
                response += f"\n\n<b>Pronunciation:</b>\n<code>{result.pronunciation}</code>"
            
            await status_msg.edit_text(response, parse_mode="HTML")
            
        except Exception as e:
            error_msg = str(e)
            if "destination language" in error_msg.lower() or "invalid" in error_msg.lower():
                await status_msg.edit_text(
                    f"❌ <b>Error:</b> Kode bahasa '<code>{target_lang}</code>' tidak valid!\n\n"
                    f"Gunakan /translate tanpa parameter untuk melihat kode bahasa yang tersedia.",
                    parse_mode="HTML"
                )
            else:
                logger.error(f"Translation error: {e}")
                await status_msg.edit_text(
                    f"❌ <b>Error:</b> Gagal menerjemahkan!\n"
                    f"<i>{error_msg}</i>",
                    parse_mode="HTML"
                )
    
    async def cmd_detect(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /detect
        Format: /detect [text]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not HAS_TRANSLATOR:
            await update.message.reply_text(
                "❌ <b>Error:</b> Library terjemahan tidak terinstall!\n\n"
                "Install dengan:\n"
                "<code>pip install googletrans==4.0.0rc1</code>",
                parse_mode="HTML"
            )
            return
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/detect [teks]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/detect Hello world</code>\n"
                "<code>/detect Bonjour le monde</code>\n"
                "<code>/detect こんにちは</code>",
                parse_mode="HTML"
            )
            return
        
        text = " ".join(context.args)
        logger.command_used("/detect", user.id, user.username)
        
        try:
            # Detect language
            status_msg = await update.message.reply_text(
                "⏳ <b>Mendeteksi bahasa...</b>",
                parse_mode="HTML"
            )
            
            result = self.translator.detect(text)
            lang_name = self.get_language_name(result.lang)
            
            # Confidence percentage
            confidence = int(result.confidence * 100)
            
            response = (
                f"🔍 <b>Deteksi Bahasa</b>\n\n"
                f"<b>Teks:</b>\n<i>{text}</i>\n\n"
                f"<b>Bahasa:</b> {lang_name} (<code>{result.lang}</code>)\n"
                f"<b>Confidence:</b> {confidence}%"
            )
            
            await status_msg.edit_text(response, parse_mode="HTML")
            
        except Exception as e:
            logger.error(f"Detection error: {e}")
            await status_msg.edit_text(
                f"❌ <b>Error:</b> Gagal mendeteksi bahasa!",
                parse_mode="HTML"
            )


# Instance plugin
plugin = TranslatePlugin()