"""
========================================
Plugin: Short URL
========================================
Nama: Short URL
Deskripsi: Plugin untuk memperpendek URL panjang
Commands:
  - /short [url]: Perpendek URL
  - /unshort [short_url]: Expand short URL
Contoh Penggunaan:
  - /short https://www.example.com/very/long/url/path
  - /unshort https://tinyurl.com/abc123
========================================
⚠️ OPTIONAL API KEY: BITLY_API_KEY or TINYURL_API_KEY
Without API key, will use free TinyURL service (no tracking)
Get Bitly API key from: https://bitly.com/a/sign_up
========================================
"""

import os
import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger


class ShortURLPlugin(PluginBase):
    """Plugin untuk memperpendek URL"""
    
    PLUGIN_NAME = "Short URL"
    PLUGIN_DESCRIPTION = "Perpendek URL panjang menjadi lebih singkat"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "utility"
    
    COMMANDS = [
        {"command": "short", "description": "Perpendek URL", "handler": "cmd_short"},
        {"command": "unshort", "description": "Expand short URL", "handler": "cmd_unshort"}
    ]
    
    EXAMPLES = [
        "/short https://www.example.com/very/long/url",
        "/unshort https://tinyurl.com/abc123"
    ]
    
    def __init__(self):
        super().__init__()
        self.bitly_token = os.getenv("BITLY_API_KEY")
        self.tinyurl_token = os.getenv("TINYURL_API_KEY")
    
    async def initialize(self):
        if not self.bitly_token and not self.tinyurl_token:
            logger.info(f"Plugin {self.PLUGIN_NAME}: No API keys configured, using free TinyURL")
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    def validate_url(self, url: str) -> bool:
        """Validate URL format"""
        return url.startswith(('http://', 'https://'))
    
    async def shorten_with_bitly(self, url: str) -> str:
        """Shorten URL using Bitly API"""
        if not self.bitly_token:
            raise ValueError("Bitly API key not configured")
        
        api_url = "https://api-ssl.bitly.com/v4/shorten"
        headers = {
            "Authorization": f"Bearer {self.bitly_token}",
            "Content-Type": "application/json"
        }
        data = {
            "long_url": url
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["link"]
                elif response.status == 400:
                    raise ValueError("URL tidak valid")
                elif response.status == 403:
                    raise ValueError("API key tidak valid")
                else:
                    raise ValueError(f"Error dari Bitly: {response.status}")
    
    async def shorten_with_tinyurl(self, url: str) -> str:
        """Shorten URL using TinyURL API"""
        # Free TinyURL API (no auth required)
        api_url = f"https://tinyurl.com/api-create.php?url={url}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    short_url = await response.text()
                    if short_url and short_url.startswith('http'):
                        return short_url.strip()
                    else:
                        raise ValueError("Gagal membuat short URL")
                else:
                    raise ValueError(f"Error dari TinyURL: {response.status}")
    
    async def expand_url(self, short_url: str) -> str:
        """Expand short URL to original URL"""
        async with aiohttp.ClientSession() as session:
            async with session.get(short_url, allow_redirects=False) as response:
                if response.status in [301, 302, 303, 307, 308]:
                    # Get redirect location
                    return response.headers.get('Location', short_url)
                elif response.status == 200:
                    # Already expanded or invalid
                    return short_url
                else:
                    raise ValueError("URL tidak valid atau sudah expired")
    
    async def cmd_short(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /short
        Format: /short [url]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/short [URL]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/short https://www.example.com/very/long/url/path</code>\n\n"
                "<i>URL akan diperpendek menggunakan TinyURL</i>",
                parse_mode="HTML"
            )
            return
        
        url = context.args[0]
        
        # Validate URL
        if not self.validate_url(url):
            await update.message.reply_text(
                "❌ <b>Error:</b> URL harus dimulai dengan http:// atau https://",
                parse_mode="HTML"
            )
            return
        
        logger.command_used("/short", user.id, user.username)
        
        try:
            # Show loading
            status_msg = await update.message.reply_text(
                "⏳ <b>Memperpendek URL...</b>",
                parse_mode="HTML"
            )
            
            # Try Bitly first if available, otherwise use TinyURL
            if self.bitly_token:
                short_url = await self.shorten_with_bitly(url)
                service = "Bitly"
            else:
                short_url = await self.shorten_with_tinyurl(url)
                service = "TinyURL"
            
            # Calculate savings
            original_length = len(url)
            short_length = len(short_url)
            saved = original_length - short_length
            saved_percent = int((saved / original_length) * 100)
            
            response = (
                f"✂️ <b>URL Diperpendek!</b>\n\n"
                f"<b>Original URL:</b>\n<code>{url[:80]}{'...' if len(url) > 80 else ''}</code>\n\n"
                f"<b>Short URL:</b>\n<code>{short_url}</code>\n\n"
                f"📊 <b>Stats:</b>\n"
                f"• Original: {original_length} karakter\n"
                f"• Short: {short_length} karakter\n"
                f"• Saved: {saved} karakter ({saved_percent}%)\n"
                f"• Service: {service}"
            )
            
            await status_msg.edit_text(response, parse_mode="HTML")
            
        except ValueError as e:
            await status_msg.edit_text(
                f"❌ <b>Error:</b> {str(e)}",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Short URL error: {e}")
            await status_msg.edit_text(
                f"❌ <b>Error:</b> Gagal memperpendek URL!",
                parse_mode="HTML"
            )
    
    async def cmd_unshort(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /unshort
        Format: /unshort [short_url]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/unshort [short URL]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/unshort https://tinyurl.com/abc123</code>\n"
                "<code>/unshort https://bit.ly/xyz789</code>",
                parse_mode="HTML"
            )
            return
        
        short_url = context.args[0]
        
        # Validate URL
        if not self.validate_url(short_url):
            await update.message.reply_text(
                "❌ <b>Error:</b> URL harus dimulai dengan http:// atau https://",
                parse_mode="HTML"
            )
            return
        
        logger.command_used("/unshort", user.id, user.username)
        
        try:
            # Show loading
            status_msg = await update.message.reply_text(
                "⏳ <b>Expanding URL...</b>",
                parse_mode="HTML"
            )
            
            # Expand URL
            original_url = await self.expand_url(short_url)
            
            if original_url == short_url:
                response = (
                    f"ℹ️ <b>URL Info</b>\n\n"
                    f"URL ini tidak mengarah ke redirect atau sudah dalam bentuk expanded.\n\n"
                    f"<b>URL:</b>\n<code>{original_url}</code>"
                )
            else:
                response = (
                    f"🔗 <b>URL Expanded!</b>\n\n"
                    f"<b>Short URL:</b>\n<code>{short_url}</code>\n\n"
                    f"<b>Original URL:</b>\n<code>{original_url[:200]}{'...' if len(original_url) > 200 else ''}</code>"
                )
            
            await status_msg.edit_text(response, parse_mode="HTML")
            
        except ValueError as e:
            await status_msg.edit_text(
                f"❌ <b>Error:</b> {str(e)}",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Unshort URL error: {e}")
            await status_msg.edit_text(
                f"❌ <b>Error:</b> Gagal expand URL!",
                parse_mode="HTML"
            )


# Instance plugin
plugin = ShortURLPlugin()