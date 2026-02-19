"""
========================================
Plugin: Fun
========================================
Nama: Fun
Deskripsi: Plugin untuk fitur fun dan entertainment
Commands:
  - /roll [sides]: Roll dadu (default 6 sides)
  - /flip: Flip koin (head/tail)
  - /joke: Random joke
  - /8ball [pertanyaan]: Magic 8-ball
Contoh Penggunaan:
  - /roll
  - /roll 20
  - /flip
  - /joke
  - /8ball Apakah aku akan sukses?
========================================
"""

import random
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger

class FunPlugin(PluginBase):
    """Plugin untuk fitur fun dan entertainment"""
    
    PLUGIN_NAME = "Fun"
    PLUGIN_DESCRIPTION = "Fitur fun dan entertainment"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "fun"
    
    COMMANDS = [
        {"command": "roll", "description": "Roll dadu", "handler": "cmd_roll"},
        {"command": "flip", "description": "Flip koin", "handler": "cmd_flip"},
        {"command": "joke", "description": "Random joke", "handler": "cmd_joke"},
        {"command": "8ball", "description": "Magic 8-ball", "handler": "cmd_8ball"}
    ]
    
    EXAMPLES = [
        "/roll",
        "/roll 20",
        "/flip",
        "/joke",
        "/8ball Apakah aku akan sukses?"
    ]
    
    # Data untuk 8-ball
    EIGHT_BALL_RESPONSES = [
        "🎱 It is certain",
        "🎱 It is decidedly so",
        "🎱 Without a doubt",
        "🎱 Yes definitely",
        "🎱 You may rely on it",
        "🎱 As I see it, yes",
        "🎱 Most likely",
        "🎱 Outlook good",
        "🎱 Yes",
        "🎱 Signs point to yes",
        "🎱 Reply hazy, try again",
        "🎱 Ask again later",
        "🎱 Better not tell you now",
        "🎱 Cannot predict now",
        "🎱 Concentrate and ask again",
        "🎱 Don't count on it",
        "🎱 My reply is no",
        "🎱 My sources say no",
        "🎱 Outlook not so good",
        "🎱 Very doubtful"
    ]
    
    # Data untuk jokes
    JOKES = [
        "Why don't scientists trust atoms? Because they make up everything! 😄",
        "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
        "Why don't eggs tell jokes? They'd crack each other up! 🥚",
        "What do you call a fake noodle? An impasta! 🍝",
        "Why did the math book look so sad? Because it had too many problems! 📚",
        "What do you call a bear with no teeth? A gummy bear! 🐻",
        "Why did the cookie go to the doctor? Because it was feeling crumbly! 🍪",
        "What do you call a sleeping dinosaur? A dino-snore! 🦕",
        "Why did the student eat his homework? Because the teacher said it was a piece of cake! 📖",
        "What do you call a fish with no eyes? Fsh! 🐟",
        "Why did the picture go to jail? Because it was framed! 🖼️",
        "What do you call a boomerang that doesn't come back? A stick! 🪃",
        "Why did the tomato turn red? Because it saw the salad dressing! 🍅",
        "What do you call a can opener that doesn't work? A can't opener! 🥫",
        "Why did the bicycle fall over? Because it was two-tired! 🚲"
    ]
    
    async def initialize(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    async def cmd_roll(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /roll
        Format: /roll atau /roll [sides]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        # Parse argumen
        sides = 6
        if context.args:
            try:
                sides = int(context.args[0])
                if sides < 2:
                    sides = 2
                elif sides > 100:
                    sides = 100
            except ValueError:
                pass
        
        logger.command_used(f"/roll {sides}", user.id, user.username)
        
        # Roll dadu
        result = random.randint(1, sides)
        
        await update.message.reply_text(
            f"🎲 <b>Roll {sides}-sided dice:</b>\n\n"
            f"Hasil: <b>{result}</b>!",
            parse_mode="HTML"
        )
    
    async def cmd_flip(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /flip
        Flip koin (head/tail)
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        logger.command_used("/flip", user.id, user.username)
        
        # Flip koin
        result = random.choice(["Heads", "Tails"])
        emoji = "👑" if result == "Heads" else "🪙"
        
        await update.message.reply_text(
            f"🪙 <b>Coin Flip:</b>\n\n"
            f"Hasil: {emoji} <b>{result}</b>!",
            parse_mode="HTML"
        )
    
    async def cmd_joke(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /joke
        Random joke
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        logger.command_used("/joke", user.id, user.username)
        
        # Pilih random joke
        joke = random.choice(self.JOKES)
        
        await update.message.reply_text(
            f"😄 <b>Random Joke:</b>\n\n"
            f"{joke}",
            parse_mode="HTML"
        )
    
    async def cmd_8ball(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /8ball
        Format: /8ball [pertanyaan]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/8ball [pertanyaan]</code>\n\n"
                "<i>Contoh: /8ball Apakah aku akan sukses?</i>",
                parse_mode="HTML"
            )
            return
        
        question = " ".join(context.args)
        logger.command_used("/8ball", user.id, user.username)
        
        # Pilih random response
        response = random.choice(self.EIGHT_BALL_RESPONSES)
        
        await update.message.reply_text(
            f"❓ <b>Pertanyaan:</b> <i>{question}</i>\n\n"
            f"{response}",
            parse_mode="HTML"
        )

# Instance plugin
plugin = FunPlugin()
