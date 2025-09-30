"""
Update checker for SavePassword
"""

import requests
import json
import sys
import os
from tkinter import messagebox

class UpdateChecker:
    """Check for application updates"""
    
    def __init__(self):
        self.current_version = "1.2.0"
        self.github_repo = "Techraym/SavePassword"
        self.latest_version = None
        self.release_info = None
    
    def check_for_updates(self):
        """Check for available updates"""
        try:
            url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            release_data = response.json()
            self.latest_version = release_data['tag_name'].lstrip('v')
            self.release_info = release_data
            
            return self.is_update_available()
        except Exception as e:
            print(f"Error checking for updates: {e}")
            return False
    
    def is_update_available(self):
        """Check if update is available"""
        if not self.latest_version:
            return False
        
        current_parts = self.parse_version(self.current_version)
        latest_parts = self.parse_version(self.latest_version)
        
        return latest_parts > current_parts
    
    def parse_version(self, version_string):
        """Parse version string into comparable tuple"""
        parts = version_string.split('.')
        # Convert each part to integer, handling non-numeric parts
        parsed_parts = []
        for part in parts:
            try:
                parsed_parts.append(int(part))
            except ValueError:
                # For non-numeric parts, use 0
                parsed_parts.append(0)
        
        # Ensure we have at least 3 parts (major.minor.patch)
        while len(parsed_parts) < 3:
            parsed_parts.append(0)
        
        return tuple(parsed_parts)
    
    def get_update_info(self):
        """Get update information"""
        if not self.release_info:
            return None
        
        return {
            'current_version': self.current_version,
            'latest_version': self.latest_version,
            'release_notes': self.release_info.get('body', ''),
            'download_url': self.release_info.get('html_url', ''),
            'published_at': self.release_info.get('published_at', '')
        }
    
    def show_update_dialog(self, parent):
        """Show update available dialog"""
        update_info = self.get_update_info()
        if not update_info:
            messagebox.showerror("Update Check", "Could not retrieve update information.")
            return
        
        message = (
            f"Current version: {update_info['current_version']}\n"
            f"Latest version: {update_info['latest_version']}\n\n"
            f"Update available!\n\n"
            f"Would you like to visit the download page?"
        )
        
        result = messagebox.askyesno("Update Available", message)
        if result:
            import webbrowser
            webbrowser.open(update_info['download_url'])
    
    def check_and_notify(self, parent):
        """Check for updates and notify user if available"""
        try:
            if self.check_for_updates():
                self.show_update_dialog(parent)
            else:
                messagebox.showinfo("Update Check", "You have the latest version.")
        except Exception as e:
            messagebox.showerror("Update Check", f"Error checking for updates: {e}")