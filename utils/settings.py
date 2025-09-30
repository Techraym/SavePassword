"""
Settings management for SavePassword
"""

import json
import os
import sys

class SettingsManager:
    """Manage application settings"""
    
    def __init__(self, settings_file=None):
        if settings_file is None:
            # Determine settings file location
            if getattr(sys, 'frozen', False):
                # Running as executable
                base_dir = os.path.dirname(sys.executable)
            else:
                # Running as script
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            settings_file = os.path.join(base_dir, "settings.json")
        
        self.settings_file = settings_file
        self.settings = self.load_default_settings()
        self.load_settings()
    
    def load_default_settings(self):
        """Load default settings"""
        return {
            'theme': 'light',
            'language': 'en',
            'auto_lock': True,
            'lock_timeout': 300,  # 5 minutes
            'clipboard_clear_time': 30,  # 30 seconds
            'backup_interval': 7,  # 7 days
            'last_database': None,
            'window_width': 1200,
            'window_height': 700,
            'window_x': None,
            'window_y': None,
            'check_updates': True,
            'minimize_to_tray': False
        }
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # Update default settings with loaded ones
                    self.settings.update(loaded_settings)
                return True
        except Exception as e:
            print(f"Error loading settings: {e}")
        return False
    
    def save_settings(self):
        """Save settings to file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
        return False
    
    def get(self, key, default=None):
        """Get setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set setting value"""
        self.settings[key] = value
        return self.save_settings()
    
    def delete(self, key):
        """Delete setting"""
        if key in self.settings:
            del self.settings[key]
            return self.save_settings()
        return False
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.load_default_settings()
        return self.save_settings()
    
    def get_all_settings(self):
        """Get all settings as dictionary"""
        return self.settings.copy()