"""
========================================
Plugin: Weather
========================================
Nama: Weather
Deskripsi: Plugin untuk mengecek informasi cuaca
Commands:
  - /weather [kota]: Cek cuaca saat ini
  - /forecast [kota]: Cek prediksi cuaca
Contoh Penggunaan:
  - /weather Jakarta
  - /weather London
  - /forecast Tokyo
========================================
⚠️ REQUIRES API KEY: OPENWEATHER_API_KEY
Get your API key from: https://openweathermap.org/api
========================================
"""

import os
import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

from core.plugin_base import PluginBase
from utils.database import db
from utils.logger import logger


class WeatherPlugin(PluginBase):
    """Plugin untuk informasi cuaca"""
    
    PLUGIN_NAME = "Weather"
    PLUGIN_DESCRIPTION = "Informasi cuaca dari OpenWeatherMap"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "System"
    PLUGIN_CATEGORY = "info"
    
    COMMANDS = [
        {"command": "weather", "description": "Cek cuaca saat ini", "handler": "cmd_weather"},
        {"command": "forecast", "description": "Prediksi cuaca", "handler": "cmd_forecast"}
    ]
    
    EXAMPLES = [
        "/weather Jakarta",
        "/weather London",
        "/forecast Tokyo"
    ]
    
    # OpenWeatherMap API
    API_BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
    
    async def initialize(self):
        if not self.api_key:
            logger.warning(f"Plugin {self.PLUGIN_NAME}: API key not configured!")
        logger.info(f"Plugin {self.PLUGIN_NAME} initialized")
    
    async def shutdown(self):
        logger.info(f"Plugin {self.PLUGIN_NAME} shutdown")
    
    def get_weather_emoji(self, weather_id: int) -> str:
        """Mendapatkan emoji berdasarkan weather condition ID"""
        if 200 <= weather_id < 300:
            return "⛈️"  # Thunderstorm
        elif 300 <= weather_id < 400:
            return "🌦️"  # Drizzle
        elif 500 <= weather_id < 600:
            return "🌧️"  # Rain
        elif 600 <= weather_id < 700:
            return "❄️"  # Snow
        elif 700 <= weather_id < 800:
            return "🌫️"  # Atmosphere (fog, mist, etc)
        elif weather_id == 800:
            return "☀️"  # Clear
        elif weather_id > 800:
            return "☁️"  # Clouds
        return "🌡️"
    
    async def fetch_weather(self, city: str) -> dict:
        """Fetch weather data dari API"""
        if not self.api_key:
            raise ValueError("API key tidak dikonfigurasi. Tambahkan OPENWEATHER_API_KEY ke .env")
        
        url = f"{self.API_BASE_URL}/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "lang": "id"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 404:
                    raise ValueError(f"Kota '{city}' tidak ditemukan")
                elif response.status == 401:
                    raise ValueError("API key tidak valid")
                elif response.status != 200:
                    raise ValueError(f"Error dari API: {response.status}")
                
                return await response.json()
    
    async def fetch_forecast(self, city: str) -> dict:
        """Fetch forecast data dari API"""
        if not self.api_key:
            raise ValueError("API key tidak dikonfigurasi. Tambahkan OPENWEATHER_API_KEY ke .env")
        
        url = f"{self.API_BASE_URL}/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "lang": "id",
            "cnt": 8  # 8 data points (24 hours)
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 404:
                    raise ValueError(f"Kota '{city}' tidak ditemukan")
                elif response.status == 401:
                    raise ValueError("API key tidak valid")
                elif response.status != 200:
                    raise ValueError(f"Error dari API: {response.status}")
                
                return await response.json()
    
    async def cmd_weather(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /weather
        Format: /weather [city]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/weather [nama kota]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/weather Jakarta</code>\n"
                "<code>/weather London</code>",
                parse_mode="HTML"
            )
            return
        
        city = " ".join(context.args)
        logger.command_used(f"/weather {city}", user.id, user.username)
        
        try:
            # Tampilkan loading
            status_msg = await update.message.reply_text("⏳ <b>Mengambil data cuaca...</b>", parse_mode="HTML")
            
            # Fetch data
            data = await self.fetch_weather(city)
            
            # Parse data
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            temp_min = data["main"]["temp_min"]
            temp_max = data["main"]["temp_max"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind_speed = data["wind"]["speed"]
            weather_desc = data["weather"][0]["description"].capitalize()
            weather_id = data["weather"][0]["id"]
            emoji = self.get_weather_emoji(weather_id)
            
            # Format response
            text = (
                f"{emoji} <b>Cuaca di {city}</b>\n\n"
                f"🌡️ <b>Suhu:</b> {temp}°C (terasa seperti {feels_like}°C)\n"
                f"📊 <b>Min/Max:</b> {temp_min}°C / {temp_max}°C\n"
                f"💧 <b>Kelembaban:</b> {humidity}%\n"
                f"🎚️ <b>Tekanan:</b> {pressure} hPa\n"
                f"💨 <b>Kecepatan Angin:</b> {wind_speed} m/s\n"
                f"☁️ <b>Kondisi:</b> {weather_desc}"
            )
            
            await status_msg.edit_text(text, parse_mode="HTML")
            
        except ValueError as e:
            await status_msg.edit_text(f"❌ <b>Error:</b> {str(e)}", parse_mode="HTML")
        except Exception as e:
            logger.error(f"Weather error: {str(e)}")
            await status_msg.edit_text(
                f"❌ <b>Error:</b> Gagal mengambil data cuaca!",
                parse_mode="HTML"
            )
    
    async def cmd_forecast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler untuk command /forecast
        Format: /forecast [city]
        """
        user = update.effective_user
        db.update_user_activity(user.id)
        
        if not context.args:
            await update.message.reply_text(
                "⚠️ <b>Penggunaan:</b>\n"
                "<code>/forecast [nama kota]</code>\n\n"
                "<b>Contoh:</b>\n"
                "<code>/forecast Jakarta</code>",
                parse_mode="HTML"
            )
            return
        
        city = " ".join(context.args)
        logger.command_used(f"/forecast {city}", user.id, user.username)
        
        try:
            # Tampilkan loading
            status_msg = await update.message.reply_text("⏳ <b>Mengambil prediksi cuaca...</b>", parse_mode="HTML")
            
            # Fetch data
            data = await self.fetch_forecast(city)
            
            # Parse forecast data (ambil 4 data point pertama = 12 jam)
            text = f"📅 <b>Prediksi Cuaca {city}</b>\n\n"
            
            for item in data["list"][:4]:
                time = item["dt_txt"].split()[1][:5]  # HH:MM
                temp = item["main"]["temp"]
                weather_desc = item["weather"][0]["description"]
                weather_id = item["weather"][0]["id"]
                emoji = self.get_weather_emoji(weather_id)
                
                text += f"{emoji} <b>{time}</b> - {temp}°C, {weather_desc}\n"
            
            await status_msg.edit_text(text, parse_mode="HTML")
            
        except ValueError as e:
            await status_msg.edit_text(f"❌ <b>Error:</b> {str(e)}", parse_mode="HTML")
        except Exception as e:
            logger.error(f"Forecast error: {str(e)}")
            await status_msg.edit_text(
                f"❌ <b>Error:</b> Gagal mengambil prediksi cuaca!",
                parse_mode="HTML"
            )


# Instance plugin
plugin = WeatherPlugin()