"""
Theme management for SavePassword
"""

import tkinter as tk
from tkinter import ttk

class ThemeManager:
    """Manage application themes"""
    
    def __init__(self):
        self.themes = {
            'light': {
                'bg': '#ffffff',
                'fg': '#000000',
                'accent': '#007acc',
                'secondary_bg': '#f0f0f0',
                'secondary_fg': '#333333',
                'button_bg': '#e1e1e1',
                'button_fg': '#000000',
                'entry_bg': '#ffffff',
                'entry_fg': '#000000',
                'select_bg': '#007acc',
                'select_fg': '#ffffff'
            },
            'dark': {
                'bg': '#2b2b2b',
                'fg': '#ffffff',
                'accent': '#007acc',
                'secondary_bg': '#3c3c3c',
                'secondary_fg': '#cccccc',
                'button_bg': '#404040',
                'button_fg': '#ffffff',
                'entry_bg': '#404040',
                'entry_fg': '#ffffff',
                'select_bg': '#007acc',
                'select_fg': '#ffffff'
            },
            'blue': {
                'bg': '#f0f8ff',
                'fg': '#000080',
                'accent': '#1e90ff',
                'secondary_bg': '#e6f3ff',
                'secondary_fg': '#000080',
                'button_bg': '#1e90ff',
                'button_fg': '#ffffff',
                'entry_bg': '#ffffff',
                'entry_fg': '#000080',
                'select_bg': '#1e90ff',
                'select_fg': '#ffffff'
            }
        }
    
    def apply_theme(self, root, theme_name):
        """Apply theme to application"""
        if theme_name not in self.themes:
            theme_name = 'light'
        
        theme = self.themes[theme_name]
        
        # Configure ttk style
        style = ttk.Style()
        
        # Configure main styles
        style.configure('.', 
                       background=theme['bg'],
                       foreground=theme['fg'],
                       fieldbackground=theme['entry_bg'])
        
        # Configure specific widget styles
        style.configure('TFrame', background=theme['bg'])
        style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
        style.configure('TButton', 
                       background=theme['button_bg'],
                       foreground=theme['button_fg'])
        style.configure('TEntry',
                       fieldbackground=theme['entry_bg'],
                       foreground=theme['entry_fg'])
        style.configure('TCombobox',
                       fieldbackground=theme['entry_bg'],
                       foreground=theme['entry_fg'])
        style.configure('Treeview',
                       background=theme['bg'],
                       foreground=theme['fg'],
                       fieldbackground=theme['bg'])
        style.configure('Treeview.Heading',
                       background=theme['secondary_bg'],
                       foreground=theme['fg'])
        
        # Configure selected items
        style.map('Treeview',
                 background=[('selected', theme['select_bg'])],
                 foreground=[('selected', theme['select_fg'])])
        
        # Apply to root window
        root.configure(background=theme['bg'])
        
        return True
    
    def get_theme_names(self):
        """Get available theme names"""
        return list(self.themes.keys())
    
    def darken_color(self, color, factor=0.7):
        """Darken a color by a factor"""
        try:
            # Convert hex to RGB
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # Darken
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
            
            # Ensure values are within bounds
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            # Convert back to hex
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color