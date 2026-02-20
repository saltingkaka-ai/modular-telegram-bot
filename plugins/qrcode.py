"""
========================================
Plugin: QR Code
========================================
Nama: QR Code
Deskripsi: Plugin untuk membuat QR Code dari teks atau URL
Commands:
  - /qr [text/url]: Generate QR code
  - /qrurl [url]: Generate QR code untuk URL
Contoh Penggunaan:
  - /qr https://github.com
  - /qr Hello World
  - /qrurl https://t.me/username
========================================
"""

import io
import qrcode
from telegram import Update
from telegram.ext import ContextTypes

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger


class QRCodePlugin(PluginBase):
    """Plugin untuk membuat QR Code"""
    
    PLUGIN_NAME = "QR Code"
    PLUGIN_DESCRIPTION = "Generate QR Code dari teks atau URL"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "utility"
    
    COMMANDS = [
        {"command": "qr", "description": "Generate QR code", "handler": "cmd_qr"},
        {"command": "qrurl", "description": "Generate QR code untuk URL", "handler": "cmd_qrurl"}
    ]
    
    EXAMPLES = [
        "/qr https://github.com",
        "/qr Hello World!",
        "/qrurl https://t.me/username"
    ]
    
    async def initialize(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    def generate_qr(self, data: str) -> io.BytesIO:
        """Generate QR code image"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes
        bio = io.BytesIO()
        img.save(bio, 'PNG')
        bio.seek(0)
        return bio
    
    async def cmd_qr(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /qr
        Format: /qr [text/url]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/qr [teks atau URL]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/qr https://github.com</code>\n"
                "<code>/qr Hello World!</code>\n"
                "<code>/qr +628123456789</code>",
                parse_mode="HTML"
            )
            return
        
        data = " ".join(context.args)
        
        # Validasi panjang data
        if len(data) > 500:
            await update.message.reply_text(
                "❌ <b>Error:</b> Teks terlalu panjang! (maksimal 500 karakter)",
                parse_mode="HTML"
            )
            return
        
        logger.command_used(f"/qr", user.id, user.username)
        
        try:
            # Generate QR code
            status_msg = await update.message.reply_text("⏳ <b>Generating QR code...</b>", parse_mode="HTML")
            
            qr_image = self.generate_qr(data)
            
            # Kirim gambar
            await update.message.reply_photo(
                photo=qr_image,
                caption=f"📱 <b>QR Code Generated</b>\n\n"
                        f"<b>Data:</b> <code>{data[:100]}{'...' if len(data) > 100 else ''}</code>",
                parse_mode="HTML"
            )
            
            # Hapus status message
            await status_msg.delete()
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Error:</b> Gagal membuat QR code!\n"
                f"<i>{str(e)}</i>",
                parse_mode="HTML"
            )
    
    async def cmd_qrurl(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /qrurl
        Format: /qrurl [url]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/qrurl [URL]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/qrurl https://github.com</code>\n"
                "<code>/qrurl https://t.me/username</code>",
                parse_mode="HTML"
            )
            return
        
        url = context.args[0]
        
        # Validasi URL sederhana
        if not url.startswith(("http://", "https://")):
            await update.message.reply_text(
                "❌ <b>Error:</b> URL harus dimulai dengan http:// atau https://",
                parse_mode="HTML"
            )
            return
        
        logger.command_used(f"/qrurl", user.id, user.username)
        
        try:
            # Generate QR code
            status_msg = await update.message.reply_text("⏳ <b>Generating QR code for URL...</b>", parse_mode="HTML")
            
            qr_image = self.generate_qr(url)
            
            # Kirim gambar
            await update.message.reply_photo(
                photo=qr_image,
                caption=f"🔗 <b>QR Code for URL</b>\n\n"
                        f"<b>URL:</b> <code>{url}</code>\n\n"
                        f"<i>Scan QR code untuk membuka URL</i>",
                parse_mode="HTML"
            )
            
            # Hapus status message
            await status_msg.delete()
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Error:</b> Gagal membuat QR code!\n"
                f"<i>{str(e)}</i>",
                parse_mode="HTML"
            )


# Instance plugin
plugin = QRCodePlugin()