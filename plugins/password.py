"""
========================================
Plugin: Password
========================================
Nama: Password
Deskripsi: Plugin untuk generate password yang kuat dan aman
Commands:
  - /password: Generate password random (12 karakter)
  - /password [length]: Generate password dengan panjang tertentu
  - /passphrase: Generate passphrase (mudah diingat)
  - /pin: Generate PIN 4-6 digit
Contoh Penggunaan:
  - /password
  - /password 16
  - /passphrase
  - /pin
========================================
"""

import random
import string
from telegram import Update
from telegram.ext import ContextTypes

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger


class PasswordPlugin(PluginBase):
    """Plugin untuk generate password"""
    
    PLUGIN_NAME = "Password"
    PLUGIN_DESCRIPTION = "Generate password dan PIN yang kuat"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "utility"
    
    COMMANDS = [
        {"command": "password", "description": "Generate password random", "handler": "cmd_password"},
        {"command": "passphrase", "description": "Generate passphrase", "handler": "cmd_passphrase"},
        {"command": "pin", "description": "Generate PIN", "handler": "cmd_pin"}
    ]
    
    EXAMPLES = [
        "/password",
        "/password 16",
        "/passphrase",
        "/pin"
    ]
    
    # Word list untuk passphrase
    WORDS = [
        "apple", "banana", "cherry", "dragon", "eagle", "forest", "garden", "house",
        "island", "jungle", "kite", "lemon", "mountain", "ninja", "ocean", "panda",
        "queen", "river", "sunset", "tiger", "umbrella", "violet", "water", "yellow",
        "zebra", "amazing", "bright", "clever", "dream", "energy", "flying", "golden",
        "happy", "infinite", "joyful", "kindness", "lightning", "magical", "noble",
        "optimist", "peaceful", "quantum", "rainbow", "sunshine", "thunder", "united",
        "victory", "wisdom", "xenon", "youthful", "zealous"
    ]
    
    async def initialize(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    def generate_password(self, length: int = 12, include_symbols: bool = True) -> str:
        """Generate random password"""
        chars = string.ascii_letters + string.digits
        if include_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Ensure password has at least one of each type
        password = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits)
        ]
        
        if include_symbols:
            password.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
        
        # Fill the rest
        password.extend(random.choice(chars) for _ in range(length - len(password)))
        
        # Shuffle
        random.shuffle(password)
        
        return ''.join(password)
    
    def generate_passphrase(self, word_count: int = 4) -> str:
        """Generate memorable passphrase"""
        words = random.sample(self.WORDS, word_count)
        # Capitalize first letter of each word
        words = [word.capitalize() for word in words]
        # Add random numbers
        number = random.randint(10, 99)
        # Add symbol
        symbol = random.choice("!@#$%^&*")
        
        return f"{'-'.join(words)}{number}{symbol}"
    
    def generate_pin(self, length: int = 4) -> str:
        """Generate PIN"""
        return ''.join(random.choice(string.digits) for _ in range(length))
    
    def calculate_strength(self, password: str) -> tuple:
        """Calculate password strength"""
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Password terlalu pendek")
        
        # Character variety
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Tidak ada huruf kapital")
        
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Tidak ada huruf kecil")
        
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Tidak ada angka")
        
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        else:
            feedback.append("Tidak ada simbol")
        
        # Determine strength
        if score >= 6:
            strength = "Sangat Kuat 💪"
            emoji = "🟢"
        elif score >= 4:
            strength = "Kuat 👍"
            emoji = "🟡"
        elif score >= 2:
            strength = "Sedang 👌"
            emoji = "🟠"
        else:
            strength = "Lemah 👎"
            emoji = "🔴"
        
        return strength, emoji, score, feedback
    
    async def cmd_password(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /password
        Format: /password atau /password [length]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        # Parse length
        length = 12
        if context.args:
            try:
                length = int(context.args[0])
                if length < 8:
                    length = 8
                elif length > 64:
                    length = 64
            except ValueError:
                await update.message.reply_text(
                    "❌ <b>Error:</b> Panjang harus berupa angka!",
                    parse_mode="HTML"
                )
                return
        
        logger.command_used(f"/password {length}", user.id, user.username)
        
        # Generate password
        password = self.generate_password(length)
        strength, emoji, score, feedback = self.calculate_strength(password)
        
        response = (
            f"🔐 <b>Password Generator</b>\n\n"
            f"<b>Password:</b> <code>{password}</code>\n\n"
            f"{emoji} <b>Kekuatan:</b> {strength}\n"
            f"📊 <b>Score:</b> {score}/7\n"
            f"📏 <b>Panjang:</b> {len(password)} karakter\n\n"
            f"<i>⚠️ Simpan password ini dengan aman!</i>"
        )
        
        await update.message.reply_text(response, parse_mode="HTML")
    
    async def cmd_passphrase(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /passphrase
        Generate memorable passphrase
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        logger.command_used("/passphrase", user.id, user.username)
        
        # Parse word count
        word_count = 4
        if context.args:
            try:
                word_count = int(context.args[0])
                if word_count < 3:
                    word_count = 3
                elif word_count > 6:
                    word_count = 6
            except ValueError:
                pass
        
        # Generate passphrase
        passphrase = self.generate_passphrase(word_count)
        strength, emoji, score, feedback = self.calculate_strength(passphrase)
        
        response = (
            f"🔑 <b>Passphrase Generator</b>\n\n"
            f"<b>Passphrase:</b> <code>{passphrase}</code>\n\n"
            f"{emoji} <b>Kekuatan:</b> {strength}\n"
            f"📊 <b>Score:</b> {score}/7\n"
            f"📏 <b>Panjang:</b> {len(passphrase)} karakter\n\n"
            f"<i>💡 Passphrase lebih mudah diingat!</i>"
        )
        
        await update.message.reply_text(response, parse_mode="HTML")
    
    async def cmd_pin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /pin
        Generate PIN
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        # Parse length
        length = 4
        if context.args:
            try:
                length = int(context.args[0])
                if length < 4:
                    length = 4
                elif length > 8:
                    length = 8
            except ValueError:
                pass
        
        logger.command_used(f"/pin {length}", user.id, user.username)
        
        # Generate PIN
        pin = self.generate_pin(length)
        
        response = (
            f"🔢 <b>PIN Generator</b>\n\n"
            f"<b>PIN:</b> <code>{pin}</code>\n\n"
            f"📏 <b>Panjang:</b> {length} digit\n\n"
            f"<i>⚠️ Jangan gunakan PIN ini untuk akun penting!</i>\n"
            f"<i>PIN lebih cocok untuk kunci lokal/sementara.</i>"
        )
        
        await update.message.reply_text(response, parse_mode="HTML")


# Instance plugin
plugin = PasswordPlugin()