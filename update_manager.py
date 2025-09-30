#!/usr/bin/env python3
"""
Update Manager for SavePassword
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox
import requests
import json

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from utils.update_checker import UpdateChecker

def check_for_updates():
    """Check for updates and show result"""
    try:
        update_checker = UpdateChecker()
        
        root = tk.Tk()
        root.withdraw()  # Hide main window
        
        if update_checker.check_for_updates():
            update_checker.show_update_dialog(root)
        else:
            messagebox.showinfo("Update Check", 
                              f"You have the latest version ({update_checker.current_version}).")
        
        root.destroy()
    except Exception as e:
        messagebox.showerror("Update Error", f"Failed to check for updates: {e}")

if __name__ == "__main__":
    check_for_updates()