"""
========================================
Modular Telegram Bot - Database Handler
========================================
Nama: Database
Deskripsi: Handler untuk database SQLite
Command: -
Usage: Import dari file lain
========================================
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from contextlib import contextmanager

class Database:
    """Class untuk mengelola database SQLite"""
    
    def __init__(self, db_path: str = "data/bot_database.db"):
        self.db_path = db_path
        self._ensure_directory()
        self._init_tables()
    
    def _ensure_directory(self):
        """Memastikan direktori database ada"""
        directory = os.path.dirname(self.db_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    @contextmanager
    def _get_connection(self):
        """Context manager untuk koneksi database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _init_tables(self):
        """Inisialisasi tabel-tabel database"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabel Users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    language_code TEXT,
                    is_bot INTEGER DEFAULT 0,
                    joined_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    last_activity TEXT DEFAULT CURRENT_TIMESTAMP,
                    message_count INTEGER DEFAULT 0,
                    is_banned INTEGER DEFAULT 0
                )
            """)
            
            # Tabel Chats
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id INTEGER PRIMARY KEY,
                    chat_type TEXT,
                    chat_title TEXT,
                    joined_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    last_activity TEXT DEFAULT CURRENT_TIMESTAMP,
                    message_count INTEGER DEFAULT 0
                )
            """)
            
            # Tabel Stats
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT DEFAULT CURRENT_DATE,
                    command TEXT,
                    user_id INTEGER,
                    count INTEGER DEFAULT 1,
                    UNIQUE(date, command, user_id)
                )
            """)
            
            # Tabel Plugins
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS plugins (
                    name TEXT PRIMARY KEY,
                    description TEXT,
                    version TEXT DEFAULT '1.0',
                    author TEXT,
                    is_active INTEGER DEFAULT 1,
                    install_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    usage_count INTEGER DEFAULT 0
                )
            """)
            
            # Tabel Settings
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    # User Methods
    def add_user(self, user_id: int, username: Optional[str] = None, 
                 first_name: Optional[str] = None, last_name: Optional[str] = None,
                 language_code: Optional[str] = None, is_bot: bool = False) -> bool:
        """Menambahkan atau update user"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO users 
                    (user_id, username, first_name, last_name, language_code, is_bot, last_activity)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user_id, username, first_name, last_name, language_code, 
                      1 if is_bot else 0, datetime.now().isoformat()))
                return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def update_user_activity(self, user_id: int):
        """Update aktivitas terakhir user"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET last_activity = ?, message_count = message_count + 1
                    WHERE user_id = ?
                """, (datetime.now().isoformat(), user_id))
        except Exception as e:
            print(f"Error updating user activity: {e}")
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Mendapatkan data user"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_all_users(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Mendapatkan semua user"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM users 
                    ORDER BY joined_date DESC 
                    LIMIT ? OFFSET ?
                """, (limit, offset))
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
    
    def get_user_count(self) -> int:
        """Mendapatkan jumlah user"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users")
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting user count: {e}")
            return 0
    
    # Stats Methods
    def log_command(self, command: str, user_id: int):
        """Mencatat penggunaan command"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO stats (date, command, user_id, count)
                    VALUES (CURRENT_DATE, ?, ?, 1)
                    ON CONFLICT(date, command, user_id) 
                    DO UPDATE SET count = count + 1
                """, (command, user_id))
        except Exception as e:
            print(f"Error logging command: {e}")
    
    def get_stats(self, days: int = 7) -> Dict[str, Any]:
        """Mendapatkan statistik penggunaan"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Total commands
                cursor.execute("""
                    SELECT SUM(count) FROM stats 
                    WHERE date >= date('now', '-{} days')
                """.format(days))
                total_commands = cursor.fetchone()[0] or 0
                
                # Top commands
                cursor.execute("""
                    SELECT command, SUM(count) as total 
                    FROM stats 
                    WHERE date >= date('now', '-{} days')
                    GROUP BY command 
                    ORDER BY total DESC 
                    LIMIT 10
                """.format(days))
                top_commands = [dict(row) for row in cursor.fetchall()]
                
                # Active users
                cursor.execute("""
                    SELECT COUNT(DISTINCT user_id) FROM stats 
                    WHERE date >= date('now', '-{} days')
                """.format(days))
                active_users = cursor.fetchone()[0] or 0
                
                return {
                    "total_commands": total_commands,
                    "active_users": active_users,
                    "top_commands": top_commands,
                    "period_days": days
                }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {"total_commands": 0, "active_users": 0, "top_commands": [], "period_days": days}
    
    # Plugin Methods
    def register_plugin(self, name: str, description: str = "", 
                       version: str = "1.0", author: str = "Unknown") -> bool:
        """Mendaftarkan plugin ke database"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO plugins 
                    (name, description, version, author, is_active, install_date)
                    VALUES (?, ?, ?, ?, 1, ?)
                """, (name, description, version, author, datetime.now().isoformat()))
                return True
        except Exception as e:
            print(f"Error registering plugin: {e}")
            return False
    
    def update_plugin_usage(self, name: str):
        """Update penggunaan plugin"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE plugins 
                    SET usage_count = usage_count + 1
                    WHERE name = ?
                """, (name,))
        except Exception as e:
            print(f"Error updating plugin usage: {e}")
    
    def get_plugin_stats(self) -> List[Dict[str, Any]]:
        """Mendapatkan statistik plugin"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM plugins ORDER BY usage_count DESC")
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting plugin stats: {e}")
            return []
    
    # Settings Methods
    def set_setting(self, key: str, value: str):
        """Menyimpan setting"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO settings (key, value, updated_at)
                    VALUES (?, ?, ?)
                """, (key, value, datetime.now().isoformat()))
        except Exception as e:
            print(f"Error setting config: {e}")
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Mendapatkan setting"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
                row = cursor.fetchone()
                return row[0] if row else default
        except Exception as e:
            print(f"Error getting config: {e}")
            return default

# Singleton instance
db = Database()
