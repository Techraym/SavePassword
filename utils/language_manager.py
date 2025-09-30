"""
Language management for SavePassword
"""

import json
import os
import sys
import requests

class LanguageManager:
    """Manage multi-language support"""
    
    def __init__(self, language_dir=None):
        if language_dir is None:
            # Determine language directory
            if getattr(sys, 'frozen', False):
                # Running as executable
                base_dir = os.path.dirname(sys.executable)
            else:
                # Running as script
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            language_dir = os.path.join(base_dir, "languages")
        
        self.language_dir = language_dir
        self.current_language = "en"
        self.translations = {}
        self.available_languages = self.discover_languages()
        
        # Load default language
        self.load_language("en")
    
    def discover_languages(self):
        """Discover available language files"""
        languages = {}
        
        # Check local language files
        if os.path.exists(self.language_dir):
            for filename in os.listdir(self.language_dir):
                if filename.endswith('.json'):
                    lang_code = filename[:-5]  # Remove .json extension
                    languages[lang_code] = {
                        'local': True,
                        'file': os.path.join(self.language_dir, filename)
                    }
        
        # Define available languages with their names
        language_names = {
            'en': 'English',
            'de': 'Deutsch',
            'fr': 'Français',
            'es': 'Español',
            'it': 'Italiano',
            'nl': 'Nederlands',
            'pl': 'Polski',
            'pt': 'Português'
        }
        
        # Add language names
        for lang_code, info in languages.items():
            info['name'] = language_names.get(lang_code, lang_code)
        
        return languages
    
    def load_language(self, language_code):
        """Load language file"""
        try:
            file_path = os.path.join(self.language_dir, f"{language_code}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.translations = json.load(f)
                self.current_language = language_code
                return True
            else:
                print(f"Language file not found: {file_path}")
                return False
        except Exception as e:
            print(f"Error loading language {language_code}: {e}")
            return False
    
    def set_language(self, language_code):
        """Set current language and save to settings"""
        if self.load_language(language_code):
            # Save to settings if available
            try:
                from utils.settings import SettingsManager
                settings_manager = SettingsManager()
                settings_manager.set('language', language_code)
            except:
                pass  # Settings might not be available yet
            return True
        return False
        
    def get(self, key, default=None):
        """Get translation for key"""
        return self.translations.get(key, default or key)
    
    def get_current_language(self):
        """Get current language code"""
        return self.current_language
    
    def get_available_languages(self):
        """Get list of available languages"""
        return self.available_languages
    
    def download_language(self, language_code):
        """Download language file from GitHub"""
        try:
            url = f"https://raw.githubusercontent.com/Techraym/SavePassword/main/languages/{language_code}.json"
            response = requests.get(url)
            response.raise_for_status()
            
            # Save language file
            os.makedirs(self.language_dir, exist_ok=True)
            file_path = os.path.join(self.language_dir, f"{language_code}.json")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Update available languages
            self.available_languages = self.discover_languages()
            
            return True
        except Exception as e:
            print(f"Error downloading language {language_code}: {e}")
            return False
    
    def is_language_available(self, language_code):
        """Check if language is available"""
        return language_code in self.available_languages
    
    def get_language_name(self, language_code):
        """Get display name for language code"""
        if language_code in self.available_languages:
            return self.available_languages[language_code].get('name', language_code)
        return language_code