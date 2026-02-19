"""
========================================
Modular Telegram Bot - Core Package
========================================
Nama: Core
Deskripsi: Package untuk core functionality (plugin base dan manager)
========================================
"""

from core.plugin_base import PluginBase, PluginInfo
from core.plugin_manager import PluginManager

__all__ = ['PluginBase', 'PluginInfo', 'PluginManager']
