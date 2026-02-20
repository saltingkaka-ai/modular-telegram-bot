"""
========================================
Plugin: Calculator
========================================
Nama: Calculator
Deskripsi: Plugin untuk melakukan perhitungan matematika
Commands:
  - /calc [expression]: Menghitung ekspresi matematika
  - /factorial [n]: Menghitung faktorial
  - /sqrt [n]: Menghitung akar kuadrat
  - /power [base] [exp]: Menghitung pangkat
Contoh Penggunaan:
  - /calc 2 + 2
  - /calc (5 * 3) + 10
  - /factorial 5
  - /sqrt 16
  - /power 2 3
========================================
"""

import math
from telegram import Update
from telegram.ext import ContextTypes

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger


class CalculatorPlugin(PluginBase):
    """Plugin untuk kalkulator dan perhitungan matematika"""
    
    PLUGIN_NAME = "Calculator"
    PLUGIN_DESCRIPTION = "Kalkulator dan perhitungan matematika"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "utility"
    
    COMMANDS = [
        {"command": "calc", "description": "Hitung ekspresi matematika", "handler": "cmd_calc"},
        {"command": "factorial", "description": "Hitung faktorial", "handler": "cmd_factorial"},
        {"command": "sqrt", "description": "Hitung akar kuadrat", "handler": "cmd_sqrt"},
        {"command": "power", "description": "Hitung pangkat", "handler": "cmd_power"}
    ]
    
    EXAMPLES = [
        "/calc 2 + 2",
        "/calc (5 * 3) + 10",
        "/factorial 5",
        "/sqrt 16",
        "/power 2 3"
    ]
    
    # Fungsi matematika yang diizinkan
    ALLOWED_FUNCTIONS = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'sqrt': math.sqrt,
        'log': math.log,
        'log10': math.log10,
        'exp': math.exp,
        'abs': abs,
        'round': round,
        'pi': math.pi,
        'e': math.e
    }
    
    async def initialize(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    def safe_eval(self, expression: str) -> float:
        """Evaluasi ekspresi matematika dengan aman"""
        # Bersihkan ekspresi
        expression = expression.replace(" ", "")
        
        # Cek karakter yang diizinkan
        allowed_chars = set("0123456789+-*/().epi")
        if not all(c in allowed_chars for c in expression.replace("sin", "").replace("cos", "").replace("tan", "").replace("sqrt", "").replace("log", "").replace("exp", "").replace("abs", "")):
            raise ValueError("Ekspresi mengandung karakter yang tidak diizinkan")
        
        # Evaluasi dengan namespace terbatas
        return eval(expression, {"__builtins__": {}}, self.ALLOWED_FUNCTIONS)
    
    async def cmd_calc(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /calc
        Format: /calc [expression]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/calc [ekspresi]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/calc 2 + 2</code>\n"
                "<code>/calc (5 * 3) + 10</code>\n"
                "<code>/calc sqrt(16)</code>\n"
                "<code>/calc sin(pi/2)</code>\n\n"
                "<b>Fungsi tersedia:</b>\n"
                "sin, cos, tan, sqrt, log, log10, exp, abs, round, pi, e",
                parse_mode="HTML"
            )
            return
        
        expression = " ".join(context.args)
        logger.command_used(f"/calc {expression}", user.id, user.username)
        
        try:
            result = self.safe_eval(expression)
            await update.message.reply_text(
                f"🧮 <b>Kalkulator</b>\n\n"
                f"<b>Ekspresi:</b> <code>{expression}</code>\n"
                f"<b>Hasil:</b> <code>{result}</code>",
                parse_mode="HTML"
            )
        except ZeroDivisionError:
            await update.message.reply_text(
                "❌ <b>Error:</b> Pembagian dengan nol!",
                parse_mode="HTML"
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Error:</b> Ekspresi tidak valid!\n"
                f"<i>{str(e)}</i>",
                parse_mode="HTML"
            )
    
    async def cmd_factorial(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /factorial
        Format: /factorial [n]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/factorial [angka]</code>\n\n"
                "<i>Contoh: /factorial 5</i>",
                parse_mode="HTML"
            )
            return
        
        try:
            n = int(context.args[0])
            if n < 0:
                await update.message.reply_text(
                    "❌ <b>Error:</b> Faktorial hanya untuk bilangan non-negatif!",
                    parse_mode="HTML"
                )
                return
            
            if n > 100:
                await update.message.reply_text(
                    "❌ <b>Error:</b> Angka terlalu besar! (maksimal 100)",
                    parse_mode="HTML"
                )
                return
            
            logger.command_used(f"/factorial {n}", user.id, user.username)
            
            result = math.factorial(n)
            await update.message.reply_text(
                f"🔢 <b>Faktorial</b>\n\n"
                f"<b>{n}!</b> = <code>{result}</code>",
                parse_mode="HTML"
            )
        except ValueError:
            await update.message.reply_text(
                "❌ <b>Error:</b> Input harus berupa angka!",
                parse_mode="HTML"
            )
    
    async def cmd_sqrt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /sqrt
        Format: /sqrt [n]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/sqrt [angka]</code>\n\n"
                "<i>Contoh: /sqrt 16</i>",
                parse_mode="HTML"
            )
            return
        
        try:
            n = float(context.args[0])
            if n < 0:
                await update.message.reply_text(
                    "❌ <b>Error:</b> Tidak bisa menghitung akar dari bilangan negatif!",
                    parse_mode="HTML"
                )
                return
            
            logger.command_used(f"/sqrt {n}", user.id, user.username)
            
            result = math.sqrt(n)
            await update.message.reply_text(
                f"√ <b>Akar Kuadrat</b>\n\n"
                f"√<b>{n}</b> = <code>{result}</code>",
                parse_mode="HTML"
            )
        except ValueError:
            await update.message.reply_text(
                "❌ <b>Error:</b> Input harus berupa angka!",
                parse_mode="HTML"
            )
    
    async def cmd_power(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /power
        Format: /power [base] [exponent]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if len(context.args) < 2:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/power [basis] [eksponen]</code>\n\n"
                "<i>Contoh: /power 2 3</i>",
                parse_mode="HTML"
            )
            return
        
        try:
            base = float(context.args[0])
            exponent = float(context.args[1])
            
            logger.command_used(f"/power {base} {exponent}", user.id, user.username)
            
            result = math.pow(base, exponent)
            await update.message.reply_text(
                f"📈 <b>Pangkat</b>\n\n"
                f"<b>{base}</b>^<b>{exponent}</b> = <code>{result}</code>",
                parse_mode="HTML"
            )
        except ValueError:
            await update.message.reply_text(
                "❌ <b>Error:</b> Input harus berupa angka!",
                parse_mode="HTML"
            )
        except OverflowError:
            await update.message.reply_text(
                "❌ <b>Error:</b> Hasil terlalu besar!",
                parse_mode="HTML"
            )


# Instance plugin
plugin = CalculatorPlugin()