"""
========================================
Plugin: Reminder
========================================
Nama: Reminder
Deskripsi: Plugin untuk membuat reminder dan timer
Commands:
  - /remind [waktu] [pesan]: Set reminder
  - /timer [detik]: Set timer countdown
  - /reminders: Lihat daftar reminder aktif
Contoh Penggunaan:
  - /remind 5m Minum obat
  - /remind 1h Meeting
  - /timer 60
  - /reminders
========================================
"""

import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger


class ReminderPlugin(PluginBase):
    """Plugin untuk reminder dan timer"""
    
    PLUGIN_NAME = "Reminder"
    PLUGIN_DESCRIPTION = "Reminder dan timer"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "utility"
    
    COMMANDS = [
        {"command": "remind", "description": "Set reminder", "handler": "cmd_remind"},
        {"command": "timer", "description": "Set timer countdown", "handler": "cmd_timer"},
        {"command": "reminders", "description": "Lihat reminder aktif", "handler": "cmd_reminders"}
    ]
    
    EXAMPLES = [
        "/remind 5m Minum obat",
        "/remind 1h Meeting dengan klien",
        "/timer 60",
        "/reminders"
    ]
    
    def __init__(self):
        super().__init__()
        # Store active reminders per user
        self.active_reminders = {}
    
    async def initialize(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    def parse_time(self, time_str: str) -> int:
        """Parse time string ke detik"""
        time_str = time_str.lower().strip()
        
        # Format: 5m, 1h, 30s, 2d
        if time_str.endswith('s'):
            return int(time_str[:-1])
        elif time_str.endswith('m'):
            return int(time_str[:-1]) * 60
        elif time_str.endswith('h'):
            return int(time_str[:-1]) * 3600
        elif time_str.endswith('d'):
            return int(time_str[:-1]) * 86400
        else:
            # Assume seconds if no unit
            return int(time_str)
    
    async def send_reminder(self, chat_id: int, message: str, user_id: int):
        """Kirim reminder ke user"""
        from bot import bot
        try:
            await bot.application.bot.send_message(
                chat_id=chat_id,
                text=f"⏰ <b>Reminder!</b>\n\n{message}",
                parse_mode="HTML"
            )
            # Remove from active reminders
            if user_id in self.active_reminders:
                self.active_reminders[user_id] = [
                    r for r in self.active_reminders[user_id] 
                    if r['message'] != message
                ]
        except Exception as e:
            logger.error(f"Failed to send reminder: {e}")
    
    async def cmd_remind(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /remind
        Format: /remind [time] [message]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if len(context.args) < 2:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/remind [waktu] [pesan]</code>\n\n"
                "<b>Format waktu:</b>\n"
                "• s = detik (contoh: 30s)\n"
                "• m = menit (contoh: 5m)\n"
                "• h = jam (contoh: 1h)\n"
                "• d = hari (contoh: 2d)\n\n"
                "<b>Contoh:</b>\n"
                "<code>/remind 5m Minum obat</code>\n"
                "<code>/remind 1h Meeting</code>\n"
                "<code>/remind 2d Bayar tagihan</code>",
                parse_mode="HTML"
            )
            return
        
        try:
            time_str = context.args[0]
            message = " ".join(context.args[1:])
            
            seconds = self.parse_time(time_str)
            
            # Validasi waktu
            if seconds < 1:
                await update.message.reply_text(
                    "❌ <b>Error:</b> Waktu minimal 1 detik!",
                    parse_mode="HTML"
                )
                return
            
            if seconds > 86400 * 30:  # Max 30 days
                await update.message.reply_text(
                    "❌ <b>Error:</b> Waktu maksimal 30 hari!",
                    parse_mode="HTML"
                )
                return
            
            logger.command_used(f"/remind {time_str} {message}", user.id, user.username)
            
            # Calculate reminder time
            remind_at = datetime.now() + timedelta(seconds=seconds)
            
            # Store reminder
            if user.id not in self.active_reminders:
                self.active_reminders[user.id] = []
            
            self.active_reminders[user.id].append({
                'message': message,
                'time': remind_at,
                'seconds': seconds
            })
            
            # Format time display
            if seconds < 60:
                time_display = f"{seconds} detik"
            elif seconds < 3600:
                time_display = f"{seconds // 60} menit"
            elif seconds < 86400:
                time_display = f"{seconds // 3600} jam"
            else:
                time_display = f"{seconds // 86400} hari"
            
            await update.message.reply_text(
                f"✅ <b>Reminder telah diset!</b>\n\n"
                f"⏰ <b>Waktu:</b> {time_display}\n"
                f"📝 <b>Pesan:</b> {message}\n"
                f"🕐 <b>Reminder pada:</b> {remind_at.strftime('%H:%M:%S')}",
                parse_mode="HTML"
            )
            
            # Schedule reminder
            await asyncio.sleep(seconds)
            await self.send_reminder(update.effective_chat.id, message, user.id)
            
        except ValueError:
            await update.message.reply_text(
                "❌ <b>Error:</b> Format waktu tidak valid!",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Remind error: {e}")
            await update.message.reply_text(
                f"❌ <b>Error:</b> Gagal membuat reminder!",
                parse_mode="HTML"
            )
    
    async def cmd_timer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /timer
        Format: /timer [seconds]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/timer [detik]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/timer 60</code> - Timer 1 menit\n"
                "<code>/timer 300</code> - Timer 5 menit",
                parse_mode="HTML"
            )
            return
        
        try:
            seconds = int(context.args[0])
            
            if seconds < 1 or seconds > 3600:
                await update.message.reply_text(
                    "❌ <b>Error:</b> Timer harus antara 1-3600 detik (1 jam)!",
                    parse_mode="HTML"
                )
                return
            
            logger.command_used(f"/timer {seconds}", user.id, user.username)
            
            await update.message.reply_text(
                f"⏱️ <b>Timer dimulai!</b>\n\n"
                f"⏰ Durasi: {seconds} detik\n"
                f"📢 Anda akan diberi tahu saat timer selesai.",
                parse_mode="HTML"
            )
            
            # Wait for timer
            await asyncio.sleep(seconds)
            
            # Send notification
            await update.message.reply_text(
                f"⏰ <b>Timer Selesai!</b>\n\n"
                f"Timer {seconds} detik telah berakhir! ⏱️",
                parse_mode="HTML"
            )
            
        except ValueError:
            await update.message.reply_text(
                "❌ <b>Error:</b> Input harus berupa angka!",
                parse_mode="HTML"
            )
    
    async def cmd_reminders(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /reminders
        Lihat daftar reminder aktif
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        logger.command_used("/reminders", user.id, user.username)
        
        if user.id not in self.active_reminders or not self.active_reminders[user.id]:
            await update.message.reply_text(
                "📋 <b>Reminder Aktif</b>\n\n"
                "<i>Tidak ada reminder aktif saat ini.</i>",
                parse_mode="HTML"
            )
            return
        
        # Build list
        text = "📋 <b>Reminder Aktif</b>\n\n"
        
        for i, reminder in enumerate(self.active_reminders[user.id], 1):
            time_left = (reminder['time'] - datetime.now()).total_seconds()
            if time_left > 0:
                if time_left < 60:
                    time_str = f"{int(time_left)}s"
                elif time_left < 3600:
                    time_str = f"{int(time_left // 60)}m"
                elif time_left < 86400:
                    time_str = f"{int(time_left // 3600)}h"
                else:
                    time_str = f"{int(time_left // 86400)}d"
                
                text += f"{i}. <b>{reminder['message']}</b>\n"
                text += f"   ⏰ {time_str} lagi ({reminder['time'].strftime('%H:%M')})\n\n"
        
        await update.message.reply_text(text, parse_mode="HTML")


# Instance plugin
plugin = ReminderPlugin()