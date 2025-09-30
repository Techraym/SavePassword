"""
Dialog windows for SavePassword
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import webbrowser
import random
import string

class DatabaseSelectionDialog:
    """Dialog for selecting or creating database"""
    
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.dialog = None
    
    def show(self):
        """Show the dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Select Database")
        self.dialog.geometry("400x200")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        ttk.Label(self.dialog, text="Choose database action:").pack(pady=20)
        
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Create New Database", 
                  command=self.create_new).pack(pady=5, fill=tk.X)
        ttk.Button(btn_frame, text="Open Existing Database", 
                  command=self.open_existing).pack(pady=5, fill=tk.X)
        ttk.Button(btn_frame, text="Use Default", 
                  command=self.use_default).pack(pady=5, fill=tk.X)
    
    def create_new(self):
        """Create new database"""
        filename = filedialog.asksaveasfilename(
            title="Create Database",
            defaultextension=".db",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )
        if filename:
            self.dialog.destroy()
            self.callback(filename)
    
    def open_existing(self):
        """Open existing database"""
        filename = filedialog.askopenfilename(
            title="Open Database",
            filetypes=[("Database files", "*.db"), ("All files", "*.*")]
        )
        if filename:
            self.dialog.destroy()
            self.callback(filename)
    
    def use_default(self):
        """Use default database"""
        self.dialog.destroy()
        self.callback("passwords.db")

class LoginDialog:
    """Login dialog"""
    
    def __init__(self, parent, password_manager, callback):
        self.parent = parent
        self.pm = password_manager
        self.callback = callback
        self.dialog = None
    
    def show(self):
        """Show login dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Login")
        self.dialog.geometry("300x150")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 100,
            self.parent.winfo_rooty() + 100
        ))
        
        ttk.Label(self.dialog, text="Enter Master Password:").pack(pady=10)
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(self.dialog, textvariable=self.password_var, show="*")
        password_entry.pack(pady=5, padx=20, fill=tk.X)
        password_entry.focus()
        
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Login", command=self.login).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to login
        password_entry.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Attempt login"""
        password = self.password_var.get()
        if self.pm.verify_master_password(password):
            self.dialog.destroy()
            self.callback()
        else:
            messagebox.showerror("Error", "Invalid master password")
    
    def cancel(self):
        """Cancel login"""
        self.dialog.destroy()
        self.parent.quit()

class SetupDialog:
    """Setup dialog for first use"""
    
    def __init__(self, parent, password_manager, callback):
        self.parent = parent
        self.pm = password_manager
        self.callback = callback
        self.dialog = None
    
    def show(self):
        """Show setup dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Setup Master Password")
        self.dialog.geometry("400x200")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        ttk.Label(self.dialog, text="Create Master Password").pack(pady=10)
        
        ttk.Label(self.dialog, text="Password:").pack()
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(self.dialog, textvariable=self.password_var, show="*")
        password_entry.pack(pady=5, padx=20, fill=tk.X)
        
        ttk.Label(self.dialog, text="Confirm Password:").pack()
        self.confirm_var = tk.StringVar()
        confirm_entry = ttk.Entry(self.dialog, textvariable=self.confirm_var, show="*")
        confirm_entry.pack(pady=5, padx=20, fill=tk.X)
        
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Create", command=self.create).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to create
        confirm_entry.bind('<Return>', lambda e: self.create())
    
    def create(self):
        """Create master password"""
        password = self.password_var.get()
        confirm = self.confirm_var.get()
        
        if not password:
            messagebox.showerror("Error", "Password cannot be empty")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        if self.pm.set_master_password(password):
            self.dialog.destroy()
            self.callback()
        else:
            messagebox.showerror("Error", "Failed to set master password")

class AddPasswordDialog:
    """Dialog for adding new password"""
    
    def __init__(self, parent, password_manager, callback):
        self.parent = parent
        self.pm = password_manager
        self.callback = callback
        self.dialog = None
    
    def show(self):
        """Show add password dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Add Password")
        self.dialog.geometry("400x400")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 100,
            self.parent.winfo_rooty() + 100
        ))
        
        # Form fields
        fields = [
            ("Title:", "title"),
            ("Username:", "username"), 
            ("Password:", "password"),
            ("Website:", "website"),
            ("Notes:", "notes")
        ]
        
        self.entries = {}
        for label_text, field_name in fields:
            ttk.Label(self.dialog, text=label_text).pack(anchor=tk.W, padx=20, pady=(10,0))
            
            if field_name == "password":
                entry_frame = ttk.Frame(self.dialog)
                entry_frame.pack(padx=20, pady=5, fill=tk.X)
                
                entry = ttk.Entry(entry_frame, show="*")
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                # Show/hide password button
                show_btn = ttk.Button(entry_frame, text="👁", width=3, 
                                    command=lambda e=entry: self.toggle_password_visibility(e))
                show_btn.pack(side=tk.RIGHT, padx=(5, 0))
                
                self.entries[field_name] = entry
                
            elif field_name == "notes":
                entry = tk.Text(self.dialog, height=4, width=40)
                entry.pack(padx=20, pady=5, fill=tk.X)
                self.entries[field_name] = entry
            else:
                entry = ttk.Entry(self.dialog)
                entry.pack(padx=20, pady=5, fill=tk.X)
                self.entries[field_name] = entry
        
        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Generate", command=self.generate).pack(side=tk.LEFT, padx=5)
    
    def toggle_password_visibility(self, entry):
        """Toggle password visibility"""
        if entry.cget('show') == '*':
            entry.config(show='')
        else:
            entry.config(show='*')
    
    def save(self):
        """Save new password"""
        data = {}
        for field_name, entry in self.entries.items():
            if field_name == "notes":
                data[field_name] = entry.get("1.0", tk.END).strip()
            else:
                data[field_name] = entry.get().strip()
        
        if not data.get('title'):
            messagebox.showerror("Error", "Title is required")
            return
        
        if not data.get('password'):
            messagebox.showerror("Error", "Password is required")
            return
        
        if self.pm.add_password(
            data['title'], data['username'], data['password'],
            data['website'], data['notes']
        ):
            self.dialog.destroy()
            self.callback()
        else:
            messagebox.showerror("Error", "Failed to save password")
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()
    
    def generate(self):
        """Generate random password"""
        length = 16
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(characters) for i in range(length))
        
        # Update password field
        password_entry = self.entries['password']
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

class SettingsDialog:
    """Settings dialog with theme, language and other options"""
    
    def __init__(self, parent, password_manager, callback):
        self.parent = parent
        self.pm = password_manager
        self.callback = callback
        self.dialog = None
        self.settings_manager = None
        self.language_manager = None
        self.theme_manager = None
        
        # Initialize managers
        from utils.settings import SettingsManager
        from utils.language_manager import LanguageManager
        from gui.themes import ThemeManager
        
        self.settings_manager = SettingsManager()
        self.language_manager = LanguageManager()
        self.theme_manager = ThemeManager()
    
    def show(self):
        """Show settings dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Settings")
        self.dialog.geometry("500x600")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 100,
            self.parent.winfo_rooty() + 50
        ))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Appearance tab
        appearance_frame = ttk.Frame(notebook)
        notebook.add(appearance_frame, text="Appearance")
        self.setup_appearance_tab(appearance_frame)
        
        # Security tab
        security_frame = ttk.Frame(notebook)
        notebook.add(security_frame, text="Security")
        self.setup_security_tab(security_frame)
        
        # Language tab
        language_frame = ttk.Frame(notebook)
        notebook.add(language_frame, text="Language")
        self.setup_language_tab(language_frame)
        
        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Save", command=self.save_settings).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Reset to Defaults", command=self.reset_defaults).pack(side=tk.LEFT, padx=5)
    
    def setup_appearance_tab(self, parent):
        """Setup appearance settings"""
        # Theme selection
        theme_frame = ttk.LabelFrame(parent, text="Theme")
        theme_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(theme_frame, text="Select Theme:").pack(anchor=tk.W, padx=5, pady=5)
        
        self.theme_var = tk.StringVar(value=self.settings_manager.get('theme', 'light'))
        themes = self.theme_manager.get_theme_names()
        
        for theme in themes:
            rb = ttk.Radiobutton(theme_frame, text=theme.capitalize(), 
                               variable=self.theme_var, value=theme)
            rb.pack(anchor=tk.W, padx=20, pady=2)
        
        # UI Settings
        ui_frame = ttk.LabelFrame(parent, text="Interface")
        ui_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Font size
        ttk.Label(ui_frame, text="Font Size:").pack(anchor=tk.W, padx=5, pady=2)
        self.font_size_var = tk.StringVar(value=str(self.settings_manager.get('font_size', 9)))
        font_combo = ttk.Combobox(ui_frame, textvariable=self.font_size_var, 
                                 values=["8", "9", "10", "11", "12"], state="readonly")
        font_combo.pack(anchor=tk.W, padx=20, pady=2, fill=tk.X)
        
        # Window behavior
        self.minimize_to_tray_var = tk.BooleanVar(value=self.settings_manager.get('minimize_to_tray', False))
        ttk.Checkbutton(ui_frame, text="Minimize to system tray", 
                       variable=self.minimize_to_tray_var).pack(anchor=tk.W, padx=5, pady=2)
        
        self.start_minimized_var = tk.BooleanVar(value=self.settings_manager.get('start_minimized', False))
        ttk.Checkbutton(ui_frame, text="Start minimized", 
                       variable=self.start_minimized_var).pack(anchor=tk.W, padx=5, pady=2)
    
    def setup_security_tab(self, parent):
        """Setup security settings"""
        # Auto-lock settings
        lock_frame = ttk.LabelFrame(parent, text="Auto Lock")
        lock_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.auto_lock_var = tk.BooleanVar(value=self.settings_manager.get('auto_lock', True))
        ttk.Checkbutton(lock_frame, text="Enable auto-lock", 
                       variable=self.auto_lock_var).pack(anchor=tk.W, padx=5, pady=2)
        
        ttk.Label(lock_frame, text="Lock after (minutes):").pack(anchor=tk.W, padx=5, pady=2)
        self.lock_timeout_var = tk.StringVar(value=str(self.settings_manager.get('lock_timeout', 5)))
        timeout_combo = ttk.Combobox(lock_frame, textvariable=self.lock_timeout_var,
                                    values=["1", "3", "5", "10", "15", "30"], state="readonly")
        timeout_combo.pack(anchor=tk.W, padx=20, pady=2, fill=tk.X)
        
        # Clipboard settings
        clipboard_frame = ttk.LabelFrame(parent, text="Clipboard")
        clipboard_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(clipboard_frame, text="Clear clipboard after (seconds):").pack(anchor=tk.W, padx=5, pady=2)
        self.clipboard_time_var = tk.StringVar(value=str(self.settings_manager.get('clipboard_clear_time', 30)))
        clipboard_combo = ttk.Combobox(clipboard_frame, textvariable=self.clipboard_time_var,
                                      values=["15", "30", "45", "60", "120"], state="readonly")
        clipboard_combo.pack(anchor=tk.W, padx=20, pady=2, fill=tk.X)
        
        # Backup settings
        backup_frame = ttk.LabelFrame(parent, text="Backup")
        backup_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(backup_frame, text="Auto-backup interval (days):").pack(anchor=tk.W, padx=5, pady=2)
        self.backup_interval_var = tk.StringVar(value=str(self.settings_manager.get('backup_interval', 7)))
        backup_combo = ttk.Combobox(backup_frame, textvariable=self.backup_interval_var,
                                   values=["1", "3", "7", "14", "30"], state="readonly")
        backup_combo.pack(anchor=tk.W, padx=20, pady=2, fill=tk.X)
    
    def setup_language_tab(self, parent):
        """Setup language settings"""
        lang_frame = ttk.LabelFrame(parent, text="Language")
        lang_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(lang_frame, text="Select Language:").pack(anchor=tk.W, padx=5, pady=5)
        
        # Get available languages
        available_languages = self.language_manager.get_available_languages()
        current_language = self.settings_manager.get('language', 'en')
        
        self.language_var = tk.StringVar(value=current_language)
        
        # Create language list
        lang_list_frame = ttk.Frame(lang_frame)
        lang_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(lang_list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create listbox
        self.lang_listbox = tk.Listbox(lang_list_frame, yscrollcommand=scrollbar.set)
        self.lang_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.lang_listbox.yview)
        
        # Add languages to listbox
        lang_codes = []
        for lang_code, lang_info in available_languages.items():
            display_name = f"{lang_info.get('name', lang_code)} ({lang_code})"
            self.lang_listbox.insert(tk.END, display_name)
            lang_codes.append(lang_code)
        
        self.available_lang_codes = lang_codes
        
        # Select current language
        if current_language in lang_codes:
            index = lang_codes.index(current_language)
            self.lang_listbox.selection_set(index)
        
        # Bind selection event
        self.lang_listbox.bind('<<ListboxSelect>>', self.on_language_select)
        
        # Download language button
        download_frame = ttk.Frame(lang_frame)
        download_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(download_frame, text="Download Selected Language", 
                  command=self.download_language).pack(side=tk.LEFT, padx=5)
        
        self.download_status = ttk.Label(download_frame, text="")
        self.download_status.pack(side=tk.LEFT, padx=5)
    
    def on_language_select(self, event):
        """Handle language selection"""
        selection = self.lang_listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.available_lang_codes):
                self.language_var.set(self.available_lang_codes[index])
    
    def download_language(self):
        """Download selected language"""
        lang_code = self.language_var.get()
        if not lang_code:
            messagebox.showwarning("Warning", "Please select a language first")
            return
        
        if self.language_manager.download_language(lang_code):
            self.download_status.config(text="Download successful!")
            messagebox.showinfo("Success", f"Language {lang_code} downloaded successfully")
        else:
            self.download_status.config(text="Download failed!")
            messagebox.showerror("Error", f"Failed to download language {lang_code}")
    
    def save_settings(self):
        """Save all settings"""
        try:
            # Appearance settings
            self.settings_manager.set('theme', self.theme_var.get())
            self.settings_manager.set('font_size', int(self.font_size_var.get()))
            self.settings_manager.set('minimize_to_tray', self.minimize_to_tray_var.get())
            self.settings_manager.set('start_minimized', self.start_minimized_var.get())
            
            # Security settings
            self.settings_manager.set('auto_lock', self.auto_lock_var.get())
            self.settings_manager.set('lock_timeout', int(self.lock_timeout_var.get()))
            self.settings_manager.set('clipboard_clear_time', int(self.clipboard_time_var.get()))
            self.settings_manager.set('backup_interval', int(self.backup_interval_var.get()))
            
            # Language settings
            self.settings_manager.set('language', self.language_var.get())
            
            # Apply language if changed
            current_lang = self.language_manager.get_current_language()
            if self.language_var.get() != current_lang:
                self.language_manager.set_language(self.language_var.get())
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.dialog.destroy()
            self.callback()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def reset_defaults(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all settings to defaults?"):
            self.settings_manager.reset_to_defaults()
            messagebox.showinfo("Success", "Settings reset to defaults!")
            self.dialog.destroy()
            self.callback()

# Placeholder classes for other dialogs
class PasswordGeneratorDialog:
    def __init__(self, parent, password_manager):
        self.parent = parent
        self.pm = password_manager
        self.dialog = None
    
    def show(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Password Generator")
        self.dialog.geometry("300x200")
        # Add generator implementation here
        ttk.Label(self.dialog, text="Password Generator - To be implemented").pack(pady=20)
        ttk.Button(self.dialog, text="Close", command=self.dialog.destroy).pack(pady=10)

class CategoryManagerDialog:
    def __init__(self, parent, password_manager, callback):
        self.parent = parent
        self.pm = password_manager
        self.callback = callback
        self.dialog = None
    
    def show(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Category Manager")
        self.dialog.geometry("400x300")
        # Add category management implementation here
        ttk.Label(self.dialog, text="Category Manager - To be implemented").pack(pady=20)
        ttk.Button(self.dialog, text="Close", command=self.dialog.destroy).pack(pady=10)

class ViewPasswordDialog:
    def __init__(self, parent, password_manager, password_id):
        self.parent = parent
        self.pm = password_manager
        self.password_id = password_id
        self.dialog = None
    
    def show(self):
        password = self.pm.get_password_by_id(self.password_id)
        if not password:
            messagebox.showerror("Error", "Password not found")
            return
        
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("View Password")
        self.dialog.geometry("400x300")
        
        # Display password details
        details = [
            f"Title: {password['title']}",
            f"Username: {password['username'] or 'N/A'}",
            f"Password: {password['password']}",
            f"Website: {password['website'] or 'N/A'}",
            f"Category: {password['category'] or 'Uncategorized'}",
            f"Notes: {password['notes'] or 'N/A'}"
        ]
        
        for detail in details:
            ttk.Label(self.dialog, text=detail).pack(anchor=tk.W, padx=20, pady=5)
        
        ttk.Button(self.dialog, text="Close", command=self.dialog.destroy).pack(pady=10)

class EditPasswordDialog:
    def __init__(self, parent, password_manager, password_id, callback):
        self.parent = parent
        self.pm = password_manager
        self.password_id = password_id
        self.callback = callback
        self.dialog = None
    
    def show(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Edit Password")
        self.dialog.geometry("400x300")
        # Add edit implementation here
        ttk.Label(self.dialog, text="Edit Password - To be implemented").pack(pady=20)
        ttk.Button(self.dialog, text="Close", command=self.dialog.destroy).pack(pady=10)

class ExportDialog:
    def __init__(self, parent, password_manager):
        self.parent = parent
        self.pm = password_manager
        self.dialog = None
    
    def show(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Export Passwords")
        self.dialog.geometry("400x200")
        # Add export implementation here
        ttk.Label(self.dialog, text="Export Passwords - To be implemented").pack(pady=20)
        ttk.Button(self.dialog, text="Close", command=self.dialog.destroy).pack(pady=10)