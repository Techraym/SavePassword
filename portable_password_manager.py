#!/usr/bin/env python3
"""
Portable SavePassword - Works without installation
"""

import os
import sys
import subprocess
import tempfile
import webbrowser

def setup_portable_environment():
    """Setup portable environment"""
    # Determine portable directory
    if getattr(sys, 'frozen', False):
        # If it's a pyinstaller executable
        portable_dir = os.path.dirname(sys.executable)
    else:
        # If it's a Python script
        portable_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create data directory
    data_dir = os.path.join(portable_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Database path for portable use
    db_path = os.path.join(data_dir, "passwords.db")
    
    return portable_dir, data_dir, db_path

def check_dependencies():
    """Check and install dependencies"""
    required_packages = ['cryptography', 'requests', 'pillow']
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} not found. Installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except:
                print(f"Could not install {package}.")
                return False
    return True

def main():
    """Main function for portable version"""
    print("Portable SavePassword")
    print("=====================")
    
    # Check dependencies
    if not check_dependencies():
        input("Press Enter to close...")
        return
    
    # Setup environment
    portable_dir, data_dir, db_path = setup_portable_environment()
    
    print(f"Data directory: {data_dir}")
    print(f"Database: {db_path}")
    print()
    
    # Import and start main application
    try:
        # Add portable directory to path
        sys.path.insert(0, portable_dir)
        
        # Import main application - CORRECTIE: main_windows ipv main_window
        from gui.main_windows import MainWindow  # ← Dit is de correctie
        from core.password_manager import PasswordManager
        import tkinter as tk
        
        # Override database path for portable use
        original_init = PasswordManager.__init__
        
        def portable_init(self, *args, **kwargs):
            # Use portable db_path if no path provided
            if len(args) == 0 and 'db_path' not in kwargs:
                kwargs['db_path'] = db_path
            original_init(self, *args, **kwargs)
        
        PasswordManager.__init__ = portable_init
        
        # Start application
        root = tk.Tk()
        app = MainWindow(root)
        root.mainloop()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to close...")

if __name__ == "__main__":
    main()