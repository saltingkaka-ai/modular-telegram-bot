"""
========================================
Plugin: Quote
========================================
Nama: Quote
Deskripsi: Plugin untuk menampilkan quotes dan kata-kata bijak
Commands:
  - /quote: Menampilkan quote random
  - /quote motivasi: Quote motivasi
  - /quote bijak: Quote bijak
  - /quote sukses: Quote tentang sukses
Contoh Penggunaan:
  - /quote
  - /quote motivasi
  - /quote bijak
========================================
"""

import random
from telegram import Update
from telegram.ext import ContextTypes

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger


class QuotePlugin(PluginBase):
    """Plugin untuk menampilkan quotes inspiratif"""
    
    PLUGIN_NAME = "Quote"
    PLUGIN_DESCRIPTION = "Quotes dan kata-kata bijak"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "fun"
    
    COMMANDS = [
        {"command": "quote", "description": "Tampilkan quote inspiratif", "handler": "cmd_quote"}
    ]
    
    EXAMPLES = [
        "/quote",
        "/quote motivasi",
        "/quote bijak",
        "/quote sukses"
    ]
    
    # Koleksi quotes berdasarkan kategori
    QUOTES = {
        "motivasi": [
            "Kesuksesan adalah jumlah dari usaha kecil yang diulang hari demi hari. 💪",
            "Jangan menunggu. Waktu tidak akan pernah 'pas'. ⏰",
            "Mulailah dari mana kamu berada. Gunakan apa yang kamu punya. Lakukan apa yang kamu bisa. 🌟",
            "Hal-hal terbaik dan terindah di dunia tidak dapat dilihat atau disentuh, tetapi harus dirasakan dengan hati. ❤️",
            "Percaya pada dirimu sendiri dan semua yang ada dalam dirimu. 🎯",
            "Kegagalan adalah kesuksesan yang tertunda. 🚀",
            "Tidak ada yang tidak mungkin, kata itu sendiri mengatakan 'Saya mungkin!' 💫",
            "Masa depan milik mereka yang percaya pada keindahan mimpi mereka. 🌈",
            "Jangan biarkan apa yang tidak bisa kamu lakukan menghalangi apa yang bisa kamu lakukan. 🏆",
            "Sukses bukan kunci kebahagiaan. Kebahagiaan adalah kunci kesuksesan. 😊"
        ],
        "bijak": [
            "Hidup adalah 10% apa yang terjadi padamu dan 90% bagaimana kamu menanggapinya. 🧘",
            "Cara terbaik untuk memprediksi masa depan adalah menciptakannya. 🔮",
            "Kesalahan adalah bukti bahwa kamu mencoba. 📚",
            "Belajarlah dari kemarin, hidup untuk hari ini, berharap untuk esok. 📅",
            "Pendidikan adalah senjata paling ampuh untuk mengubah dunia. 🎓",
            "Pikiran adalah segalanya. Apa yang kamu pikirkan, itulah yang kamu jadi. 🧠",
            "Kebahagiaan bukan sesuatu yang siap pakai. Itu datang dari tindakanmu sendiri. ☮️",
            "Jangan menilai setiap hari dari panen yang kamu tuai, tapi dari benih yang kamu tanam. 🌱",
            "Waktu yang kamu nikmati adalah waktu yang tidak terbuang. ⏳",
            "Kualitas tidak pernah kebetulan; itu selalu hasil dari niat tinggi. 🎨"
        ],
        "sukses": [
            "Sukses adalah kemampuan untuk bergerak dari satu kegagalan ke kegagalan lain tanpa kehilangan antusiasme. 🔥",
            "Jalan menuju sukses dan jalan menuju kegagalan hampir sama persis. 🛤️",
            "Sukses biasanya datang kepada mereka yang terlalu sibuk untuk mencarinya. 💼",
            "Kesempatan tidak terjadi. Kamu menciptakannya. 🎯",
            "Jangan takut untuk menyerah pada yang baik demi mengejar yang hebat. 🌟",
            "Saya tidak gagal. Saya hanya menemukan 10.000 cara yang tidak berhasil. 💡",
            "Kesuksesan sejati adalah ketika kamu takut akan sesuatu, lalu kamu melakukannya! 🦁",
            "Tidak ada elevator menuju kesuksesan. Kamu harus naik tangga. 🪜",
            "Jangan membandingkan dirimu dengan orang lain. Bandingkan dirimu dengan dirimu kemarin. 📊",
            "Kesuksesan adalah perjalanan, bukan tujuan. 🛣️"
        ],
        "cinta": [
            "Cinta adalah hal terindah yang bisa kita berikan dan terima. ❤️",
            "Di mana ada cinta, di situ ada kehidupan. 💕",
            "Cinta tidak melihat dengan mata, tetapi dengan hati. 💖",
            "Cinta sejati tidak pernah memiliki akhir yang bahagia, karena cinta sejati tidak pernah berakhir. 💝",
            "Hal terbaik yang bisa kamu pegang dalam hidup adalah satu sama lain. 🤝",
            "Cinta adalah ketika kebahagiaan orang lain lebih penting dari kebahagiaanmu sendiri. 💗",
            "Cinta tidak berarti saling menatap, tetapi melihat ke arah yang sama. 👫",
            "Jatuh cinta adalah mudah. Tetap jatuh cinta adalah istimewa. 💑",
            "Cinta dimulai dengan senyuman, tumbuh dengan ciuman, dan berakhir dengan air mata. 😊",
            "Yang penting bukan kita temukan cinta yang sempurna, tapi kita sempurnakan cinta yang kita temukan. 🌹"
        ],
        "hidup": [
            "Hidup ini terlalu singkat untuk tidak bahagia. 😄",
            "Hidup adalah apa yang terjadi padamu saat kamu sibuk membuat rencana lain. 📝",
            "Tujuan hidup adalah untuk hidup dengan tujuan. 🎯",
            "Hidup dimulai di akhir zona nyamanmu. 🌍",
            "Hidup adalah seperti mengendarai sepeda. Untuk menjaga keseimbangan, kamu harus terus bergerak. 🚴",
            "Hidup tidak diukur dari jumlah napas yang kita ambil, tapi dari momen yang mengambil napas kita. 🌟",
            "Dalam hidup, tidak ada yang perlu ditakuti. Hanya perlu dipahami. 🧐",
            "Hidup adalah 10% apa yang terjadi dan 90% bagaimana kita bereaksi. 🎭",
            "Hidup tidak sempurna, tapi outfitmu bisa. 👗",
            "Jalani hidup seolah setiap hari adalah hari terakhirmu. ⚡"
        ]
    }
    
    async def initialize(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    async def cmd_quote(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /quote
        Format: /quote atau /quote [kategori]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        # Tentukan kategori
        category = None
        if context.args:
            category = context.args[0].lower()
        
        # Pilih quote
        if category and category in self.QUOTES:
            quotes = self.QUOTES[category]
            category_name = category.capitalize()
        else:
            # Random dari semua kategori
            all_quotes = []
            for cat_quotes in self.QUOTES.values():
                all_quotes.extend(cat_quotes)
            quotes = all_quotes
            category_name = "Random"
        
        quote = random.choice(quotes)
        
        logger.command_used(f"/quote {category if category else ''}", user.id, user.username)
        
        # Buat text dengan info kategori yang tersedia
        text = f"💬 <b>Quote {category_name}</b>\n\n"
        text += f"<i>{quote}</i>\n\n"
        text += "<b>Kategori tersedia:</b>\n"
        text += "• motivasi • bijak • sukses\n"
        text += "• cinta • hidup"
        
        await update.message.reply_text(text, parse_mode="HTML")


# Instance plugin
plugin = QuotePlugin()