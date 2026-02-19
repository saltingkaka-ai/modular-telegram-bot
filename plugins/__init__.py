"""
========================================
Modular Telegram Bot - Plugins Package
========================================
Nama: Plugins
Deskripsi: Package untuk semua plugin bot
========================================

Cara membuat plugin baru:
1. Buat file .py di folder ini
2. Buat class yang meng-extend PluginBase
3. Implementasikan method yang diperlukan
4. Buat instance plugin di akhir file

Contoh:
```python
from core.plugin_base import PluginBase

class MyPlugin(PluginBase):
    PLUGIN_NAME = "MyPlugin"
    PLUGIN_DESCRIPTION = "Deskripsi plugin"
    PLUGIN_VERSION = "1.0"
    PLUGIN_AUTHOR = "Your Name"
    PLUGIN_CATEGORY = "utility"
    
    COMMANDS = [
        {"command": "mycommand", "description": "Deskripsi", "handler": "cmd_mycommand"}
    ]
    
    async def initialize(self):
        pass
    
    async def shutdown(self):
        pass
    
    async def cmd_mycommand(self, update, context):
        await update.message.reply_text("Hello!")

plugin = MyPlugin()
```
"""
