"""
========================================
Modular Telegram Bot - Plugin Manager
========================================
Nama: PluginManager
Deskripsi: Manager untuk mengelola semua plugin
Command: -
Usage: Digunakan oleh bot utama untuk load/unload plugin
========================================
"""

import os
import sys
import importlib
import importlib.util
from typing import Dict, List, Type, Optional, Any
from pathlib import Path

from core.plugin_base import PluginBase
from utils.logger import logger
from utils.database import db

class PluginManager:
    """
    Manager untuk mengelola lifecycle semua plugin.
    Menangani loading, unloading, dan registrasi plugin.
    """
    
    def __init__(self, plugins_folder: str = "plugins"):
        self.plugins_folder = plugins_folder
        self._plugins: Dict[str, PluginBase] = {}
        self._plugin_classes: Dict[str, Type[PluginBase]] = {}
        self._handlers: Dict[str, List] = {}
    
    @property
    def plugins(self) -> Dict[str, PluginBase]:
        """Dictionary plugin yang sudah diload"""
        return self._plugins.copy()
    
    @property
    def plugin_count(self) -> int:
        """Jumlah plugin yang diload"""
        return len(self._plugins)
    
    def get_plugin(self, name: str) -> Optional[PluginBase]:
        """Mendapatkan plugin berdasarkan nama"""
        return self._plugins.get(name)
    
    def get_all_plugins(self) -> List[PluginBase]:
        """Mendapatkan semua plugin yang diload"""
        return list(self._plugins.values())
    
    def get_plugin_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Mendapatkan informasi plugin"""
        plugin = self._plugins.get(name)
        if plugin:
            return plugin.info.to_dict()
        return None
    
    def get_all_plugin_info(self) -> List[Dict[str, Any]]:
        """Mendapatkan informasi semua plugin"""
        return [plugin.info.to_dict() for plugin in self._plugins.values()]
    
    def discover_plugins(self) -> List[str]:
        """
        Mendiscover semua file plugin di folder plugins.
        Returns: List nama file plugin (tanpa ekstensi)
        """
        plugin_files = []
        
        if not os.path.exists(self.plugins_folder):
            logger.warning(f"Plugins folder '{self.plugins_folder}' not found!")
            os.makedirs(self.plugins_folder, exist_ok=True)
            return plugin_files
        
        for file in os.listdir(self.plugins_folder):
            if file.endswith(".py") and not file.startswith("__"):
                plugin_name = file[:-3]  # Remove .py
                plugin_files.append(plugin_name)
        
        return sorted(plugin_files)
    
    def load_plugin(self, plugin_name: str) -> bool:
        """
        Load single plugin dari file.
        
        Args:
            plugin_name: Nama file plugin (tanpa .py)
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            plugin_path = os.path.join(self.plugins_folder, f"{plugin_name}.py")
            
            if not os.path.exists(plugin_path):
                logger.error(f"Plugin file not found: {plugin_path}")
                return False
            
            # Load module
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if spec is None or spec.loader is None:
                logger.error(f"Cannot create spec for plugin: {plugin_name}")
                return False
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin_name] = module
            spec.loader.exec_module(module)
            
            # Cari class yang meng-extend PluginBase
            plugin_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, PluginBase) and 
                    attr is not PluginBase):
                    plugin_class = attr
                    break
            
            if plugin_class is None:
                logger.error(f"No PluginBase subclass found in {plugin_name}")
                return False
            
            # Instansiasi plugin
            plugin = plugin_class()
            
            # Simpan ke dictionary
            self._plugin_classes[plugin_name] = plugin_class
            self._plugins[plugin_name] = plugin
            
            # Register ke database
            db.register_plugin(
                name=plugin.PLUGIN_NAME,
                description=plugin.PLUGIN_DESCRIPTION,
                version=plugin.PLUGIN_VERSION,
                author=plugin.PLUGIN_AUTHOR
            )
            
            logger.plugin_loaded(plugin.PLUGIN_NAME)
            return True
            
        except Exception as e:
            logger.plugin_error(plugin_name, str(e))
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload plugin.
        
        Args:
            plugin_name: Nama plugin yang akan di-unload
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            if plugin_name not in self._plugins:
                logger.warning(f"Plugin {plugin_name} is not loaded")
                return False
            
            plugin = self._plugins[plugin_name]
            
            # Panggil shutdown method
            # Note: Ini async, perlu di-handle dengan cara khusus
            # Untuk sekarang kita skip async shutdown
            
            # Hapus dari dictionary
            del self._plugins[plugin_name]
            if plugin_name in self._plugin_classes:
                del self._plugin_classes[plugin_name]
            if plugin_name in self._handlers:
                del self._handlers[plugin_name]
            
            # Hapus dari sys.modules
            if plugin_name in sys.modules:
                del sys.modules[plugin_name]
            
            logger.info(f"📤 Plugin unloaded: {plugin_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error unloading plugin {plugin_name}: {e}")
            return False
    
    def load_all_plugins(self) -> Dict[str, bool]:
        """
        Load semua plugin yang ditemukan.
        
        Returns:
            Dictionary {plugin_name: success_status}
        """
        results = {}
        plugin_files = self.discover_plugins()
        
        logger.info(f"🔍 Found {len(plugin_files)} plugin(s)")
        
        for plugin_name in plugin_files:
            success = self.load_plugin(plugin_name)
            results[plugin_name] = success
        
        # Log summary
        success_count = sum(1 for v in results.values() if v)
        logger.info(f"✅ Loaded {success_count}/{len(plugin_files)} plugin(s)")
        
        return results
    
    def reload_plugin(self, plugin_name: str) -> bool:
        """
        Reload plugin (unload lalu load lagi).
        
        Args:
            plugin_name: Nama plugin yang akan di-reload
        
        Returns:
            True jika berhasil, False jika gagal
        """
        if plugin_name in self._plugins:
            self.unload_plugin(plugin_name)
        return self.load_plugin(plugin_name)
    
    def reload_all_plugins(self) -> Dict[str, bool]:
        """
        Reload semua plugin.
        
        Returns:
            Dictionary {plugin_name: success_status}
        """
        # Simpan nama plugin yang sudah diload
        loaded_plugins = list(self._plugins.keys())
        
        # Unload semua
        for plugin_name in loaded_plugins:
            self.unload_plugin(plugin_name)
        
        # Load ulang
        return self.load_all_plugins()
    
    def get_handlers_for_application(self) -> List:
        """
        Mendapatkan semua handlers untuk didaftarkan ke Application.
        
        Returns:
            List of handlers
        """
        all_handlers = []
        
        for plugin_name, plugin in self._plugins.items():
            handlers = plugin.get_handlers()
            self._handlers[plugin_name] = handlers
            all_handlers.extend(handlers)
        
        return all_handlers
    
    async def initialize_all_plugins(self):
        """Inisialisasi semua plugin yang sudah diload"""
        for plugin_name, plugin in self._plugins.items():
            try:
                await plugin.initialize()
            except Exception as e:
                logger.error(f"Error initializing plugin {plugin_name}: {e}")
    
    async def shutdown_all_plugins(self):
        """Shutdown semua plugin"""
        for plugin_name, plugin in self._plugins.items():
            try:
                await plugin.shutdown()
            except Exception as e:
                logger.error(f"Error shutting down plugin {plugin_name}: {e}")
    
    def get_plugins_by_category(self, category: str) -> List[PluginBase]:
        """Mendapatkan plugin berdasarkan kategori"""
        return [p for p in self._plugins.values() if p.PLUGIN_CATEGORY == category]
    
    def search_plugins(self, query: str) -> List[PluginBase]:
        """Mencari plugin berdasarkan nama atau deskripsi"""
        query = query.lower()
        results = []
        
        for plugin in self._plugins.values():
            if (query in plugin.PLUGIN_NAME.lower() or 
                query in plugin.PLUGIN_DESCRIPTION.lower()):
                results.append(plugin)
        
        return results
