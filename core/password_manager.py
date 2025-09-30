"""
Password Manager Core Logic
"""

import sqlite3
import json
import hashlib
import secrets
from datetime import datetime
from core.crypto import CryptoManager

class PasswordManager:
    """Main password management class"""
    
    def __init__(self, db_path="passwords.db"):
        self.db_path = db_path
        self.crypto = CryptoManager()
        self.initialize_database()
    
    def initialize_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                parent_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES categories (id)
            )
        ''')
        
        # Passwords table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                username TEXT,
                encrypted_password TEXT NOT NULL,
                website TEXT,
                notes TEXT,
                category_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def is_master_password_set(self):
        """Check if master password is set"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = 'master_password_hash'")
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except:
            return False
    
    def set_master_password(self, password):
        """Set master password"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        stored_hash = f"{salt}:{password_hash.hex()}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            ('master_password_hash', stored_hash)
        )
        conn.commit()
        conn.close()
        
        # Set encryption key
        self.crypto.set_key_from_password(password)
        return True
    
    def verify_master_password(self, password):
        """Verify master password"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = 'master_password_hash'")
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return False
            
            stored_hash = result[0]
            salt, stored_password_hash = stored_hash.split(':')
            
            # Verify password
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            
            if password_hash.hex() == stored_password_hash:
                # Set encryption key
                self.crypto.set_key_from_password(password)
                return True
            
            return False
        except:
            return False
    
    def add_password(self, title, username, password, website="", notes="", category_id=None):
        """Add new password"""
        try:
            encrypted_password = self.crypto.encrypt(password)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO passwords (title, username, encrypted_password, website, notes, category_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, username, encrypted_password, website, notes, category_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding password: {e}")
            return False
    
    def update_password(self, password_id, title, username, password, website="", notes="", category_id=None):
        """Update existing password"""
        try:
            encrypted_password = self.crypto.encrypt(password)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE passwords 
                SET title=?, username=?, encrypted_password=?, website=?, notes=?, category_id=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            ''', (title, username, encrypted_password, website, notes, category_id, password_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False
    
    def get_all_passwords(self):
        """Get all passwords"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.id, p.title, p.username, p.encrypted_password, p.website, p.notes, 
                       c.name as category_name, p.created_at, p.updated_at
                FROM passwords p
                LEFT JOIN categories c ON p.category_id = c.id
                ORDER BY p.title
            ''')
            passwords = cursor.fetchall()
            conn.close()
            
            # Convert to list of dictionaries and decrypt passwords
            decrypted_passwords = []
            for pwd in passwords:
                try:
                    decrypted_password = self.crypto.decrypt(pwd[3])
                except:
                    decrypted_password = "***ENCRYPTED***"
                
                decrypted_passwords.append({
                    'id': pwd[0],
                    'title': pwd[1],
                    'username': pwd[2],
                    'password': decrypted_password,
                    'website': pwd[4],
                    'notes': pwd[5],
                    'category': pwd[6],
                    'created_at': pwd[7],
                    'updated_at': pwd[8]
                })
            
            return decrypted_passwords
        except Exception as e:
            print(f"Error getting passwords: {e}")
            return []
    
    def get_password_by_id(self, password_id):
        """Get password by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.id, p.title, p.username, p.encrypted_password, p.website, p.notes, 
                       c.name as category_name
                FROM passwords p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.id = ?
            ''', (password_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                try:
                    decrypted_password = self.crypto.decrypt(result[3])
                except:
                    decrypted_password = "***ENCRYPTED***"
                
                return {
                    'id': result[0],
                    'title': result[1],
                    'username': result[2],
                    'password': decrypted_password,
                    'website': result[4],
                    'notes': result[5],
                    'category': result[6]
                }
            return None
        except Exception as e:
            print(f"Error getting password: {e}")
            return None
    
    def delete_password(self, password_id):
        """Delete password by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords WHERE id = ?", (password_id,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            print(f"Error deleting password: {e}")
            return False
    
    def add_category(self, name, parent_id=None):
        """Add new category"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categories (name, parent_id) VALUES (?, ?)",
                (name, parent_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding category: {e}")
            return False
    
    def get_all_categories_flat(self):
        """Get all categories as flat list"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, parent_id FROM categories ORDER BY name")
            categories = cursor.fetchall()
            conn.close()
            
            # Convert to list of dictionaries
            return [{'id': cat[0], 'name': cat[1], 'parent_id': cat[2]} for cat in categories]
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    def get_category_tree(self):
        """Get categories as hierarchical tree"""
        flat_categories = self.get_all_categories_flat()
        return self._build_category_tree(flat_categories)
    
    def _build_category_tree(self, categories, parent_id=None):
        """Build hierarchical category tree"""
        tree = []
        for category in categories:
            if category['parent_id'] == parent_id:
                children = self._build_category_tree(categories, category['id'])
                category['children'] = children
                tree.append(category)
        return tree
    
    def search_passwords(self, query):
        """Search passwords by title, username, website, or notes"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.id, p.title, p.username, p.encrypted_password, p.website, p.notes, 
                       c.name as category_name
                FROM passwords p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.title LIKE ? OR p.username LIKE ? OR p.website LIKE ? OR p.notes LIKE ?
                ORDER BY p.title
            ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
            passwords = cursor.fetchall()
            conn.close()
            
            # Convert to list of dictionaries and decrypt passwords
            decrypted_passwords = []
            for pwd in passwords:
                try:
                    decrypted_password = self.crypto.decrypt(pwd[3])
                except:
                    decrypted_password = "***ENCRYPTED***"
                
                decrypted_passwords.append({
                    'id': pwd[0],
                    'title': pwd[1],
                    'username': pwd[2],
                    'password': decrypted_password,
                    'website': pwd[4],
                    'notes': pwd[5],
                    'category': pwd[6]
                })
            
            return decrypted_passwords
        except Exception as e:
            print(f"Error searching passwords: {e}")
            return []

# Voor backward compatibility
PasswordManagerCore = PasswordManager