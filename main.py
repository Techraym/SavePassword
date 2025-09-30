#!/usr/bin/env python3
"""
SavePassword - Main Entry Point
"""

import os
import sys
import tkinter as tk

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from gui.main_window import MainWindow
from utils.settings import SettingsManager

def main():
    """Main application entry point"""
    try:
        # Initialize settings
        settings_manager = SettingsManager()
        
        # Create main window
        root = tk.Tk()
        
        # Set application icon if exists
        try:
            icon_path = os.path.join(current_dir, "gui", "icons", "app_icon.ico")
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        except:
            pass  # Icon not critical
        
        # Start application
        app = MainWindow(root)
        root.mainloop()
        
    except Exception as e:
        print(f"Failed to start application: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to close...")

if __name__ == "__main__":
    main()