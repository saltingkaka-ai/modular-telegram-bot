"""
========================================
Plugin: Poll
========================================
Nama: Poll
Deskripsi: Plugin untuk membuat polling di grup
Commands:
  - /poll [question]: Buat polling
  - /quiz [question]: Buat quiz dengan jawaban benar
Contoh Penggunaan:
  - /poll Makan dimana? | Pizza | Burger | Sushi
  - /quiz Ibu kota Indonesia? | Jakarta | Bandung | Surabaya | 1
========================================
"""

from telegram import Update, Poll
from telegram.ext import ContextTypes

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger


class PollPlugin(PluginBase):
    """Plugin untuk membuat polling"""
    
    PLUGIN_NAME = "Poll"
    PLUGIN_DESCRIPTION = "Membuat polling dan quiz interaktif"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "utility"
    
    COMMANDS = [
        {"command": "poll", "description": "Buat polling", "handler": "cmd_poll"},
        {"command": "quiz", "description": "Buat quiz", "handler": "cmd_quiz"}
    ]
    
    EXAMPLES = [
        "/poll Makan dimana? | Pizza | Burger | Sushi",
        "/poll Setuju? | Ya | Tidak",
        "/quiz Ibu kota Indonesia? | Jakarta | Bandung | Surabaya | 1"
    ]
    
    async def initialize(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    def parse_poll_data(self, text: str) -> tuple:
        """Parse poll data dari text"""
        parts = [p.strip() for p in text.split('|')]
        
        if len(parts) < 3:
            raise ValueError("Format tidak valid. Minimal question dan 2 opsi diperlukan.")
        
        question = parts[0]
        options = parts[1:]
        
        if len(options) < 2:
            raise ValueError("Poll harus memiliki minimal 2 opsi.")
        
        if len(options) > 10:
            raise ValueError("Poll maksimal memiliki 10 opsi.")
        
        return question, options
    
    def parse_quiz_data(self, text: str) -> tuple:
        """Parse quiz data dari text"""
        parts = [p.strip() for p in text.split('|')]
        
        if len(parts) < 4:
            raise ValueError("Format tidak valid. Minimal question, 2 opsi, dan nomor jawaban benar.")
        
        question = parts[0]
        
        # Last part should be the answer index
        try:
            correct_answer = int(parts[-1]) - 1  # Convert to 0-indexed
            options = parts[1:-1]
            
            if correct_answer < 0 or correct_answer >= len(options):
                raise ValueError("Nomor jawaban benar tidak valid.")
            
        except ValueError:
            raise ValueError("Nomor jawaban benar harus berupa angka.")
        
        if len(options) < 2:
            raise ValueError("Quiz harus memiliki minimal 2 opsi.")
        
        if len(options) > 10:
            raise ValueError("Quiz maksimal memiliki 10 opsi.")
        
        return question, options, correct_answer
    
    async def cmd_poll(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /poll
        Format: /poll [question] | [option1] | [option2] | ...
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/poll [pertanyaan] | [opsi1] | [opsi2] | ...</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/poll Makan dimana? | Pizza | Burger | Sushi</code>\n"
                "<code>/poll Setuju dengan proposal? | Ya | Tidak | Abstain</code>\n\n"
                "<b>Catatan:</b>\n"
                "• Gunakan | untuk memisahkan pertanyaan dan opsi\n"
                "• Minimal 2 opsi, maksimal 10 opsi\n"
                "• Poll bisa di-share ke grup atau channel",
                parse_mode="HTML"
            )
            return
        
        try:
            text = " ".join(context.args)
            question, options = self.parse_poll_data(text)
            
            logger.command_used(f"/poll", user.id, user.username)
            
            # Send poll
            await context.bot.send_poll(
                chat_id=update.effective_chat.id,
                question=question,
                options=options,
                is_anonymous=True,
                allows_multiple_answers=False
            )
            
            # Delete command message for cleaner look
            try:
                await update.message.delete()
            except:
                pass
            
        except ValueError as e:
            await update.message.reply_text(
                f"❌ <b>Error:</b> {str(e)}",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Poll error: {e}")
            await update.message.reply_text(
                "❌ <b>Error:</b> Gagal membuat poll!",
                parse_mode="HTML"
            )
    
    async def cmd_quiz(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /quiz
        Format: /quiz [question] | [option1] | [option2] | ... | [correct_answer_number]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/quiz [pertanyaan] | [opsi1] | [opsi2] | ... | [nomor jawaban benar]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/quiz Ibu kota Indonesia? | Jakarta | Bandung | Surabaya | 1</code>\n"
                "<code>/quiz 2+2=? | 3 | 4 | 5 | 2</code>\n\n"
                "<b>Catatan:</b>\n"
                "• Gunakan | untuk memisahkan\n"
                "• Nomor terakhir adalah jawaban benar (1, 2, 3, dst)\n"
                "• Minimal 2 opsi, maksimal 10 opsi\n"
                "• Quiz akan menampilkan jawaban benar setelah dijawab",
                parse_mode="HTML"
            )
            return
        
        try:
            text = " ".join(context.args)
            question, options, correct_answer = self.parse_quiz_data(text)
            
            logger.command_used(f"/quiz", user.id, user.username)
            
            # Send quiz
            await context.bot.send_poll(
                chat_id=update.effective_chat.id,
                question=question,
                options=options,
                type=Poll.QUIZ,
                correct_option_id=correct_answer,
                is_anonymous=True,
                explanation=f"Jawaban yang benar adalah: {options[correct_answer]}"
            )
            
            # Delete command message for cleaner look
            try:
                await update.message.delete()
            except:
                pass
            
        except ValueError as e:
            await update.message.reply_text(
                f"❌ <b>Error:</b> {str(e)}",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Quiz error: {e}")
            await update.message.reply_text(
                "❌ <b>Error:</b> Gagal membuat quiz!",
                parse_mode="HTML"
            )


# Instance plugin
plugin = PollPlugin()