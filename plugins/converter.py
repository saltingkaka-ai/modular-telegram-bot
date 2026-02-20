"""
========================================
Plugin: Converter
========================================
Nama: Converter
Deskripsi: Plugin untuk konversi berbagai unit pengukuran
Commands:
  - /convert [nilai] [dari] [ke]: Konversi unit
  - /currency [nilai] [dari] [ke]: Konversi mata uang
  - /temp [nilai] [dari] [ke]: Konversi suhu
Contoh Penggunaan:
  - /convert 100 km mile
  - /convert 5 kg lb
  - /temp 100 c f
  - /temp 32 f c
========================================
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger


class ConverterPlugin(PluginBase):
    """Plugin untuk konversi unit"""
    
    PLUGIN_NAME = "Converter"
    PLUGIN_DESCRIPTION = "Konversi berbagai unit pengukuran"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "utility"
    
    COMMANDS = [
        {"command": "convert", "description": "Konversi unit pengukuran", "handler": "cmd_convert"},
        {"command": "temp", "description": "Konversi suhu", "handler": "cmd_temp"}
    ]
    
    EXAMPLES = [
        "/convert 100 km mile",
        "/convert 5 kg lb",
        "/temp 100 c f",
        "/temp 32 f c"
    ]
    
    # Conversion factors to base unit
    UNITS = {
        # Length (base: meter)
        "length": {
            "km": 1000,
            "m": 1,
            "cm": 0.01,
            "mm": 0.001,
            "mile": 1609.34,
            "yard": 0.9144,
            "foot": 0.3048,
            "ft": 0.3048,
            "inch": 0.0254,
            "in": 0.0254
        },
        # Weight (base: kg)
        "weight": {
            "ton": 1000,
            "kg": 1,
            "gram": 0.001,
            "g": 0.001,
            "mg": 0.000001,
            "lb": 0.453592,
            "pound": 0.453592,
            "oz": 0.0283495,
            "ounce": 0.0283495
        },
        # Volume (base: liter)
        "volume": {
            "kl": 1000,
            "liter": 1,
            "l": 1,
            "ml": 0.001,
            "gallon": 3.78541,
            "gal": 3.78541,
            "quart": 0.946353,
            "pint": 0.473176,
            "cup": 0.236588
        },
        # Area (base: m²)
        "area": {
            "km2": 1000000,
            "m2": 1,
            "cm2": 0.0001,
            "hectare": 10000,
            "ha": 10000,
            "acre": 4046.86,
            "sqft": 0.092903,
            "sqin": 0.00064516
        },
        # Speed (base: m/s)
        "speed": {
            "mps": 1,
            "kph": 0.277778,
            "kmh": 0.277778,
            "mph": 0.44704,
            "knot": 0.514444
        }
    }
    
    async def initialize(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    def find_unit_category(self, unit: str) -> str:
        """Mencari kategori unit"""
        unit = unit.lower()
        for category, units in self.UNITS.items():
            if unit in units:
                return category
        return None
    
    def convert_unit(self, value: float, from_unit: str, to_unit: str) -> float:
        """Konversi dari satu unit ke unit lain"""
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        # Cari kategori
        category = self.find_unit_category(from_unit)
        if not category or category != self.find_unit_category(to_unit):
            raise ValueError("Unit tidak kompatibel atau tidak ditemukan")
        
        # Konversi ke base unit, lalu ke target unit
        base_value = value * self.UNITS[category][from_unit]
        result = base_value / self.UNITS[category][to_unit]
        
        return result
    
    def convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float:
        """Konversi suhu"""
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        # Konversi ke Celsius dulu
        if from_unit == "c" or from_unit == "celsius":
            celsius = value
        elif from_unit == "f" or from_unit == "fahrenheit":
            celsius = (value - 32) * 5/9
        elif from_unit == "k" or from_unit == "kelvin":
            celsius = value - 273.15
        else:
            raise ValueError("Unit suhu tidak valid (gunakan: c, f, k)")
        
        # Konversi dari Celsius ke target
        if to_unit == "c" or to_unit == "celsius":
            return celsius
        elif to_unit == "f" or to_unit == "fahrenheit":
            return (celsius * 9/5) + 32
        elif to_unit == "k" or to_unit == "kelvin":
            return celsius + 273.15
        else:
            raise ValueError("Unit suhu tidak valid (gunakan: c, f, k)")
    
    async def cmd_convert(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /convert
        Format: /convert [nilai] [dari] [ke]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if len(context.args) < 3:
            # Tampilkan bantuan
            help_text = (
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/convert [nilai] [dari] [ke]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/convert 100 km mile</code>\n"
                "<code>/convert 5 kg lb</code>\n"
                "<code>/convert 1 gallon liter</code>\n\n"
                "<b>Unit yang didukung:</b>\n\n"
                "<b>Panjang:</b> km, m, cm, mm, mile, yard, ft, inch\n"
                "<b>Berat:</b> ton, kg, g, mg, lb, oz\n"
                "<b>Volume:</b> liter (l), ml, gallon, quart, pint, cup\n"
                "<b>Area:</b> km2, m2, cm2, hectare (ha), acre, sqft\n"
                "<b>Kecepatan:</b> mps, kph, mph, knot"
            )
            await update.message.reply_text(help_text, parse_mode="HTML")
            return
        
        try:
            value = float(context.args[0])
            from_unit = context.args[1]
            to_unit = context.args[2]
            
            logger.command_used(f"/convert {value} {from_unit} {to_unit}", user.id, user.username)
            
            result = self.convert_unit(value, from_unit, to_unit)
            
            await update.message.reply_text(
                f"🔄 <b>Konversi Unit</b>\n\n"
                f"<b>{value} {from_unit}</b> = <code>{result:.4f} {to_unit}</code>",
                parse_mode="HTML"
            )
            
        except ValueError as e:
            await update.message.reply_text(
                f"❌ <b>Error:</b> {str(e)}\n\n"
                f"Gunakan /convert tanpa parameter untuk melihat unit yang didukung.",
                parse_mode="HTML"
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Error:</b> Input tidak valid!",
                parse_mode="HTML"
            )
    
    async def cmd_temp(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /temp
        Format: /temp [nilai] [dari] [ke]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if len(context.args) < 3:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/temp [nilai] [dari] [ke]</code>\n\n"
                "<b>Unit suhu:</b> c (Celsius), f (Fahrenheit), k (Kelvin)\n\n"
                "<b>Contoh:</b>\n"
                "<code>/temp 100 c f</code>\n"
                "<code>/temp 32 f c</code>\n"
                "<code>/temp 273.15 k c</code>",
                parse_mode="HTML"
            )
            return
        
        try:
            value = float(context.args[0])
            from_unit = context.args[1]
            to_unit = context.args[2]
            
            logger.command_used(f"/temp {value} {from_unit} {to_unit}", user.id, user.username)
            
            result = self.convert_temperature(value, from_unit, to_unit)
            
            # Format unit dengan huruf kapital yang sesuai
            from_label = {"c": "°C", "f": "°F", "k": "K"}.get(from_unit.lower(), from_unit)
            to_label = {"c": "°C", "f": "°F", "k": "K"}.get(to_unit.lower(), to_unit)
            
            await update.message.reply_text(
                f"🌡️ <b>Konversi Suhu</b>\n\n"
                f"<b>{value}{from_label}</b> = <code>{result:.2f}{to_label}</code>",
                parse_mode="HTML"
            )
            
        except ValueError as e:
            await update.message.reply_text(
                f"❌ <b>Error:</b> {str(e)}",
                parse_mode="HTML"
            )
        except Exception as e:
            await update.message.reply_text(
                f"❌ <b>Error:</b> Input tidak valid!",
                parse_mode="HTML"
            )


# Instance plugin
plugin = ConverterPlugin()