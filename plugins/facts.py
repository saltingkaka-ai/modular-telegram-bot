"""
========================================
Plugin: Facts
========================================
Nama: Facts
Deskripsi: Plugin untuk menampilkan fakta-fakta menarik
Commands:
  - /fact: Tampilkan fakta random
  - /fact science: Fakta sains
  - /fact tech: Fakta teknologi
  - /fact history: Fakta sejarah
  - /fact animal: Fakta hewan
Contoh Penggunaan:
  - /fact
  - /fact science
  - /fact tech
========================================
"""

import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger


class FactsPlugin(PluginBase):
    """Plugin untuk menampilkan fakta menarik"""
    
    PLUGIN_NAME = "Facts"
    PLUGIN_DESCRIPTION = "Fakta-fakta menarik dari berbagai kategori"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "fun"
    
    COMMANDS = [
        {"command": "fact", "description": "Tampilkan fakta menarik", "handler": "cmd_fact"}
    ]
    
    EXAMPLES = [
        "/fact",
        "/fact science",
        "/fact tech",
        "/fact history"
    ]
    
    # Koleksi fakta berdasarkan kategori
    FACTS = {
        "science": [
            "🔬 Air panas membeku lebih cepat daripada air dingin. Fenomena ini disebut Efek Mpemba.",
            "🔬 Tubuh manusia mengandung cukup karbon untuk membuat 900 pensil.",
            "🔬 DNA manusia 99.9% identik satu sama lain.",
            "🔬 Cahaya dari matahari membutuhkan sekitar 8 menit untuk sampai ke Bumi.",
            "🔬 Otak manusia menggunakan 20% dari total energi tubuh, meskipun hanya 2% dari berat tubuh.",
            "🔬 Air di Bumi lebih tua dari Matahari.",
            "🔬 Emas bisa dimakan dan tidak beracun. Bahkan digunakan di beberapa makanan mewah!",
            "🔬 Petir 5 kali lebih panas dari permukaan Matahari.",
            "🔬 Satu sendok teh bintang neutron beratnya sekitar 6 miliar ton.",
            "🔬 Kecepatan cahaya adalah 299,792,458 meter per detik."
        ],
        "tech": [
            "💻 Email pertama dikirim pada tahun 1971 oleh Ray Tomlinson.",
            "💻 Nama Google berasal dari kata 'googol', angka 1 diikuti 100 nol.",
            "💻 Domain pertama yang pernah didaftarkan adalah Symbolics.com pada 1985.",
            "💻 Mouse komputer pertama dibuat dari kayu pada tahun 1964.",
            "💻 Emoji pertama dibuat di Jepang pada tahun 1999.",
            "💻 Lebih dari 6 miliar password dicuri dalam 10 tahun terakhir.",
            "💻 Kamera pertama membutuhkan 8 jam eksposur untuk mengambil satu foto.",
            "💻 WiFi adalah singkatan dari Wireless Fidelity.",
            "💻 Komputer pertama beratnya 27 ton dan mengisi seluruh ruangan.",
            "💻 90% mata uang dunia hanya ada dalam bentuk digital."
        ],
        "history": [
            "📜 Cleopatra hidup lebih dekat dengan waktu pendaratan di bulan daripada pembangunan Piramida Giza.",
            "📜 Napoleon Bonaparte sebenarnya tidak pendek. Tingginya rata-rata untuk zamannya.",
            "📜 Universitas Oxford lebih tua dari Kerajaan Aztec.",
            "📜 Tembok Besar China tidak terlihat dari luar angkasa.",
            "📜 Julius Caesar diculik oleh bajak laut dan menuntut mereka menaikkan tebusan.",
            "📜 Albert Einstein bisa saja menjadi Presiden Israel, tapi dia menolak.",
            "📜 Perang terpendek dalam sejarah berlangsung 38-45 menit.",
            "📜 Ketchup dijual sebagai obat pada tahun 1830an.",
            "📜 Bendera Amerika dirancang oleh siswa SMA sebagai proyek sekolah.",
            "📜 Piramida Giza dibangun saat mammoth masih hidup."
        ],
        "animal": [
            "🐾 Kucing memiliki 32 otot di setiap telinga.",
            "🐾 Jerapah tidak memiliki pita suara dan hampir tidak bersuara.",
            "🐾 Gurita memiliki tiga jantung dan darah berwarna biru.",
            "🐾 Berang-berang laut tidur sambil bergandengan tangan agar tidak terpisah.",
            "🐾 Penguin hanya memiliki satu pasangan seumur hidup.",
            "🐾 Hiu sudah ada sejak sebelum pohon ada di Bumi.",
            "🐾 Lebah madu bisa mengenali wajah manusia.",
            "🐾 Kuda laut jantan yang hamil dan melahirkan, bukan betina.",
            "🐾 Kecoak bisa hidup seminggu tanpa kepala.",
            "🐾 Gajah adalah satu-satunya mamalia yang tidak bisa melompat.",
            "🐾 Koloni semut terbesar panjangnya 6.000 km dari Italia ke Spanyol.",
            "🐾 Flamingo berwarna pink karena makanan mereka."
        ],
        "space": [
            "🌌 Ada lebih banyak bintang di alam semesta daripada butiran pasir di Bumi.",
            "🌌 Satu hari di Venus lebih lama dari satu tahun di Venus.",
            "🌌 Jupiter sangat besar sehingga 1.300 Bumi bisa muat di dalamnya.",
            "🌌 Tidak ada suara di luar angkasa karena tidak ada udara untuk merambatkan gelombang suara.",
            "🌌 Saturnus bisa mengapung di air karena kepadatannya lebih rendah.",
            "🌌 Jejak kaki astronot di Bulan bisa bertahan jutaan tahun.",
            "🌌 Matahari adalah 99.86% dari massa total tata surya kita.",
            "🌌 Lubang hitam bisa menyedot cahaya, tapi tidak bisa dilihat langsung.",
            "🌌 Neptunus memiliki angin tercepat di tata surya, mencapai 2.100 km/jam.",
            "🌌 Bintang berkedip karena atmosfer Bumi, bukan karena bintangnya sendiri."
        ],
        "food": [
            "🍕 Pizza Margherita dinamai dari Ratu Margherita dari Italia.",
            "🍕 Madu tidak pernah basi. Madu 3000 tahun yang lalu masih bisa dimakan.",
            "🍕 Wortel aslinya berwarna ungu, bukan oranye.",
            "🍕 Cokelat dulu digunakan sebagai mata uang oleh suku Aztec.",
            "🍕 Apel mengapung di air karena 25% kandungannya adalah udara.",
            "🍕 Pisang adalah berry, tapi stroberi bukan berry.",
            "🍕 Peanut (kacang tanah) sebenarnya bukan kacang, tapi kacang-kacangan.",
            "🍕 Wasabi yang kita makan biasanya bukan wasabi asli, tapi lobak horseradish.",
            "🍕 Nanas membutuhkan 2 tahun untuk tumbuh.",
            "🍕 Kentang adalah sayuran pertama yang ditanam di luar angkasa."
        ]
    }
    
    def __init__(self):
        super().__init__()
        # Register callback handler for "another fact" button
        self.add_handler(CallbackQueryHandler(self.cb_another_fact, pattern="^fact_"))
    
    async def initialize(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    def get_category_emoji(self, category: str) -> str:
        """Get emoji for category"""
        emojis = {
            "science": "🔬",
            "tech": "💻",
            "history": "📜",
            "animal": "🐾",
            "space": "🌌",
            "food": "🍕"
        }
        return emojis.get(category, "💡")
    
    async def cmd_fact(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /fact
        Format: /fact atau /fact [category]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        # Determine category
        category = None
        if context.args:
            category = context.args[0].lower()
        
        # Get fact
        if category and category in self.FACTS:
            facts = self.FACTS[category]
            category_name = category.capitalize()
        else:
            # Random from all categories
            all_facts = []
            for cat, cat_facts in self.FACTS.items():
                all_facts.extend([(cat, fact) for fact in cat_facts])
            
            category, fact = random.choice(all_facts)
            category_name = category.capitalize()
            facts = [fact]
            fact = facts[0]
        
        if category in self.FACTS:
            fact = random.choice(facts)
        
        logger.command_used(f"/fact {category if category else ''}", user.id, user.username)
        
        # Create keyboard
        keyboard = [
            [InlineKeyboardButton("🔄 Fakta Lain", callback_data=f"fact_{category}")],
            [InlineKeyboardButton("🔬 Science", callback_data="fact_science"),
             InlineKeyboardButton("💻 Tech", callback_data="fact_tech")],
            [InlineKeyboardButton("📜 History", callback_data="fact_history"),
             InlineKeyboardButton("🐾 Animal", callback_data="fact_animal")],
            [InlineKeyboardButton("🌌 Space", callback_data="fact_space"),
             InlineKeyboardButton("🍕 Food", callback_data="fact_food")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Build text
        emoji = self.get_category_emoji(category)
        text = f"{emoji} <b>Fakta {category_name}</b>\n\n{fact}"
        
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=reply_markup)
    
    async def cb_another_fact(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for another fact callback"""
        query = update.callback_query
        await query.answer()
        
        user = update.effective_user
        db.update_user_activity(user.id)
        
        # Get category from callback data
        category = query.data.split("_")[1]
        
        # Get random fact
        if category in self.FACTS:
            fact = random.choice(self.FACTS[category])
            category_name = category.capitalize()
        else:
            # Random from all
            all_facts = []
            for cat, cat_facts in self.FACTS.items():
                all_facts.extend([(cat, fact) for fact in cat_facts])
            
            category, fact = random.choice(all_facts)
            category_name = category.capitalize()
        
        # Create keyboard
        keyboard = [
            [InlineKeyboardButton("🔄 Fakta Lain", callback_data=f"fact_{category}")],
            [InlineKeyboardButton("🔬 Science", callback_data="fact_science"),
             InlineKeyboardButton("💻 Tech", callback_data="fact_tech")],
            [InlineKeyboardButton("📜 History", callback_data="fact_history"),
             InlineKeyboardButton("🐾 Animal", callback_data="fact_animal")],
            [InlineKeyboardButton("🌌 Space", callback_data="fact_space"),
             InlineKeyboardButton("🍕 Food", callback_data="fact_food")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Build text
        emoji = self.get_category_emoji(category)
        text = f"{emoji} <b>Fakta {category_name}</b>\n\n{fact}"
        
        await query.edit_message_text(text, parse_mode="HTML", reply_markup=reply_markup)


# Instance plugin
plugin = FactsPlugin()