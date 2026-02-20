"""
========================================
Plugin: Encode
========================================
Nama: Encode
Deskripsi: Plugin untuk encoding, decoding, dan hashing
Commands:
  - /base64enc [text]: Encode ke Base64
  - /base64dec [text]: Decode dari Base64
  - /hash [text]: Generate hash (MD5, SHA256)
  - /urlencode [text]: URL encode
  - /urldecode [text]: URL decode
Contoh Penggunaan:
  - /base64enc Hello World
  - /base64dec SGVsbG8gV29ybGQ=
  - /hash mysecretpassword
  - /urlencode Hello World!
========================================
"""

import base64
import hashlib
from urllib.parse import quote, unquote
from telegram import Update
from telegram.ext import ContextTypes

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger


class EncodePlugin(PluginBase):
    """Plugin untuk encoding, decoding, dan hashing"""
    
    PLUGIN_NAME = "Encode"
    PLUGIN_DESCRIPTION = "Encoding, decoding, dan hashing utilities"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "utility"
    
    COMMANDS = [
        {"command": "base64enc", "description": "Encode ke Base64", "handler": "cmd_base64enc"},
        {"command": "base64dec", "description": "Decode dari Base64", "handler": "cmd_base64dec"},
        {"command": "hash", "description": "Generate hash", "handler": "cmd_hash"},
        {"command": "urlencode", "description": "URL encode", "handler": "cmd_urlencode"},
        {"command": "urldecode", "description": "URL decode", "handler": "cmd_urldecode"}
    ]
    
    EXAMPLES = [
        "/base64enc Hello World",
        "/base64dec SGVsbG8gV29ybGQ=",
        "/hash mysecretpassword",
        "/urlencode Hello World!"
    ]
    
    async def initialize(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    async def cmd_base64enc(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /base64enc
        Format: /base64enc [text]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/base64enc [teks]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/base64enc Hello World</code>",
                parse_mode="HTML"
            )
            return
        
        text = " ".join(context.args)
        logger.command_used(f"/base64enc", user.id, user.username)
        
        try:
            # Encode to base64
            encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            
            await update.message.reply_text(
                f"🔐 <b>Base64 Encode</b>\n\n"
                f"<b>Original:</b>\n<code>{text}</code>\n\n"
                f"<b>Encoded:</b>\n<code>{encoded}</code>",
                parse_mode="HTML"
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Error:</b> Gagal encode!\n<i>{str(e)}</i>",
                parse_mode="HTML"
            )
    
    async def cmd_base64dec(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /base64dec
        Format: /base64dec [base64_text]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/base64dec [base64 teks]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/base64dec SGVsbG8gV29ybGQ=</code>",
                parse_mode="HTML"
            )
            return
        
        encoded = " ".join(context.args)
        logger.command_used(f"/base64dec", user.id, user.username)
        
        try:
            # Decode from base64
            decoded = base64.b64decode(encoded.encode('utf-8')).decode('utf-8')
            
            await update.message.reply_text(
                f"🔓 <b>Base64 Decode</b>\n\n"
                f"<b>Encoded:</b>\n<code>{encoded}</code>\n\n"
                f"<b>Decoded:</b>\n<code>{decoded}</code>",
                parse_mode="HTML"
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Error:</b> Input bukan Base64 yang valid!\n<i>{str(e)}</i>",
                parse_mode="HTML"
            )
    
    async def cmd_hash(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /hash
        Format: /hash [text]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/hash [teks]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/hash mysecretpassword</code>\n\n"
                "<i>Akan generate MD5, SHA1, SHA256, dan SHA512</i>",
                parse_mode="HTML"
            )
            return
        
        text = " ".join(context.args)
        logger.command_used(f"/hash", user.id, user.username)
        
        try:
            # Generate various hashes
            text_bytes = text.encode('utf-8')
            
            md5_hash = hashlib.md5(text_bytes).hexdigest()
            sha1_hash = hashlib.sha1(text_bytes).hexdigest()
            sha256_hash = hashlib.sha256(text_bytes).hexdigest()
            sha512_hash = hashlib.sha512(text_bytes).hexdigest()
            
            response = (
                f"🔐 <b>Hash Generator</b>\n\n"
                f"<b>Original:</b>\n<code>{text}</code>\n\n"
                f"<b>MD5:</b>\n<code>{md5_hash}</code>\n\n"
                f"<b>SHA1:</b>\n<code>{sha1_hash}</code>\n\n"
                f"<b>SHA256:</b>\n<code>{sha256_hash}</code>\n\n"
                f"<b>SHA512:</b>\n<code>{sha512_hash}</code>"
            )
            
            await update.message.reply_text(response, parse_mode="HTML")
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Error:</b> Gagal generate hash!\n<i>{str(e)}</i>",
                parse_mode="HTML"
            )
    
    async def cmd_urlencode(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /urlencode
        Format: /urlencode [text]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/urlencode [teks]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/urlencode Hello World!</code>",
                parse_mode="HTML"
            )
            return
        
        text = " ".join(context.args)
        logger.command_used(f"/urlencode", user.id, user.username)
        
        try:
            # URL encode
            encoded = quote(text)
            
            await update.message.reply_text(
                f"🔗 <b>URL Encode</b>\n\n"
                f"<b>Original:</b>\n<code>{text}</code>\n\n"
                f"<b>Encoded:</b>\n<code>{encoded}</code>",
                parse_mode="HTML"
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Error:</b> Gagal encode!\n<i>{str(e)}</i>",
                parse_mode="HTML"
            )
    
    async def cmd_urldecode(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /urldecode
        Format: /urldecode [encoded_url]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/urldecode [URL encoded teks]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/urldecode Hello%20World%21</code>",
                parse_mode="HTML"
            )
            return
        
        encoded = " ".join(context.args)
        logger.command_used(f"/urldecode", user.id, user.username)
        
        try:
            # URL decode
            decoded = unquote(encoded)
            
            await update.message.reply_text(
                f"🔗 <b>URL Decode</b>\n\n"
                f"<b>Encoded:</b>\n<code>{encoded}</code>\n\n"
                f"<b>Decoded:</b>\n<code>{decoded}</code>",
                parse_mode="HTML"
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Error:</b> Gagal decode!\n<i>{str(e)}</i>",
                parse_mode="HTML"
            )


# Instance plugin
plugin = EncodePlugin()