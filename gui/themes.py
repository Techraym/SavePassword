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
                'name': 'Light',
                'bg': '#ffffff',
                'fg': '#000000',
                'accent': '#007acc',
                'secondary_bg': '#f0f0f0',
                'secondary_fg': '#333333',
                'button_bg': '#e1e1e1',
                'button_fg': '#000000',
                'button_hover_bg': '#d0d0d0',
                'entry_bg': '#ffffff',
                'entry_fg': '#000000',
                'select_bg': '#007acc',
                'select_fg': '#ffffff',
                'border': '#cccccc',
                'success': '#4CAF50',
                'warning': '#FF9800',
                'error': '#F44336'
            },
            'dark': {
                'name': 'Dark',
                'bg': '#2b2b2b',
                'fg': '#ffffff',
                'accent': '#007acc',
                'secondary_bg': '#3c3c3c',
                'secondary_fg': '#cccccc',
                'button_bg': '#404040',
                'button_fg': '#ffffff',
                'button_hover_bg': '#505050',
                'entry_bg': '#404040',
                'entry_fg': '#ffffff',
                'select_bg': '#007acc',
                'select_fg': '#ffffff',
                'border': '#555555',
                'success': '#4CAF50',
                'warning': '#FF9800',
                'error': '#F44336'
            },
            'blue': {
                'name': 'Blue',
                'bg': '#f0f8ff',
                'fg': '#000080',
                'accent': '#1e90ff',
                'secondary_bg': '#e6f3ff',
                'secondary_fg': '#000080',
                'button_bg': '#1e90ff',
                'button_fg': '#ffffff',
                'button_hover_bg': '#187bcd',
                'entry_bg': '#ffffff',
                'entry_fg': '#000080',
                'select_bg': '#1e90ff',
                'select_fg': '#ffffff',
                'border': '#b0c4de',
                'success': '#228B22',
                'warning': '#FF8C00',
                'error': '#DC143C'
            },
            'green': {
                'name': 'Green',
                'bg': '#f0fff0',
                'fg': '#006400',
                'accent': '#32cd32',
                'secondary_bg': '#e6ffe6',
                'secondary_fg': '#006400',
                'button_bg': '#32cd32',
                'button_fg': '#ffffff',
                'button_hover_bg': '#28a428',
                'entry_bg': '#ffffff',
                'entry_fg': '#006400',
                'select_bg': '#32cd32',
                'select_fg': '#ffffff',
                'border': '#98fb98',
                'success': '#228B22',
                'warning': '#FF8C00',
                'error': '#DC143C'
            }
        }
    
    def apply_theme(self, root, theme_name):
        """Apply theme to application"""
        if theme_name not in self.themes:
            theme_name = 'light'
        
        theme = self.themes[theme_name]
        
        # Configure ttk style
        style = ttk.Style()
        
        try:
            # Configure main styles
            style.configure('.', 
                           background=theme['bg'],
                           foreground=theme['fg'],
                           fieldbackground=theme['entry_bg'],
                           selectbackground=theme['select_bg'],
                           selectforeground=theme['select_fg'],
                           borderwidth=1,
                           focuscolor=theme['accent'])
            
            # Configure specific widget styles
            style.configure('TFrame', background=theme['bg'])
            style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
            style.configure('TButton', 
                           background=theme['button_bg'],
                           foreground=theme['button_fg'],
                           focuscolor=theme['accent'])
            style.configure('TEntry',
                           fieldbackground=theme['entry_bg'],
                           foreground=theme['entry_fg'],
                           insertcolor=theme['fg'])
            style.configure('TCombobox',
                           fieldbackground=theme['entry_bg'],
                           foreground=theme['entry_fg'],
                           background=theme['button_bg'])
            style.configure('Treeview',
                           background=theme['bg'],
                           foreground=theme['fg'],
                           fieldbackground=theme['bg'],
                           rowheight=25)
            style.configure('Treeview.Heading',
                           background=theme['secondary_bg'],
                           foreground=theme['fg'],
                           relief='flat')
            style.configure('TNotebook',
                           background=theme['bg'],
                           tabmargins=[2, 5, 2, 0])
            style.configure('TNotebook.Tab',
                           background=theme['secondary_bg'],
                           foreground=theme['fg'],
                           padding=[10, 5])
            style.configure('TLabelframe',
                           background=theme['bg'],
                           foreground=theme['fg'])
            style.configure('TLabelframe.Label',
                           background=theme['bg'],
                           foreground=theme['fg'])
            style.configure('TScrollbar',
                           background=theme['secondary_bg'],
                           troughcolor=theme['bg'],
                           borderwidth=0)
            
            # Configure selected items
            style.map('Treeview',
                     background=[('selected', theme['select_bg'])],
                     foreground=[('selected', theme['select_fg'])])
            
            style.map('TButton',
                     background=[('active', theme['button_hover_bg']),
                                ('pressed', theme['accent'])])
            
            style.map('TNotebook.Tab',
                     background=[('selected', theme['accent']),
                                ('active', theme['button_hover_bg'])],
                     foreground=[('selected', theme['select_fg']),
                                ('active', theme['fg'])])
            
            # Apply to root window
            root.configure(background=theme['bg'])
            
            return True
            
        except Exception as e:
            print(f"Error applying theme {theme_name}: {e}")
            return False
    
    def get_theme_names(self):
        """Get available theme names"""
        return list(self.themes.keys())
    
    def get_theme_display_names(self):
        """Get theme display names"""
        return {code: theme['name'] for code, theme in self.themes.items()}
    
    def darken_color(self, color, factor=0.7):
        """Darken a color by a factor"""
        try:
            # Convert hex to RGB
            if color.startswith('#'):
                color = color[1:]
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            
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
    
    def lighten_color(self, color, factor=0.7):
        """Lighten a color by a factor"""
        try:
            # Convert hex to RGB
            if color.startswith('#'):
                color = color[1:]
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            
            # Lighten
            r = int(r + (255 - r) * factor)
            g = int(g + (255 - g) * factor)
            b = int(b + (255 - b) * factor)
            
            # Ensure values are within bounds
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            # Convert back to hex
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color