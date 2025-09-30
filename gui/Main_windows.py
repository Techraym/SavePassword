"""
Hoofdvenster voor SavePassword GUI
"""

import tkinter as tk
from tkinter import ttk
import os

from core.password_manager import PasswordManager
from gui.dialogs import *
from gui.components import CategoryExplorer, PasswordList
from gui.themes import ThemeManager
from utils.settings import SettingsManager
from utils.language_manager import LanguageManager

class MainWindow:
    """Hoofdvenster klasse voor SavePassword"""
    
    def __init__(self, root):
        self.root = root
        self.pm = None
        self.settings_manager = SettingsManager()
        self.language_manager = LanguageManager()
        self.theme_manager = ThemeManager()
        
        self.setup_window()
        self.show_database_selection()
    
    def setup_window(self):
        """Stel het hoofdvenster in"""
        self.root.title("SavePassword - Password Manager")
        self.root.geometry("1200x700")
        self.root.minsize(800, 600)
        
        # Apply theme
        theme = self.settings_manager.get('theme', 'light')
        self.theme_manager.apply_theme(self.root, theme)
    
    def show_database_selection(self):
        """Toon database selectie dialoog"""
        dialog = DatabaseSelectionDialog(self.root, self.on_database_selected)
        dialog.show()
    
    def on_database_selected(self, db_path):
        """Callback wanneer database is geselecteerd"""
        self.pm = PasswordManager(db_path)
        self.check_master_password()
    
    def check_master_password(self):
        """Controleer of master wachtwoord is ingesteld"""
        if self.pm.is_master_password_set():
            self.show_login_dialog()
        else:
            self.show_setup_dialog()
    
    def show_login_dialog(self):
        """Toon login dialoog"""
        dialog = LoginDialog(self.root, self.pm.db_path, self.on_login_success)
        dialog.show()
    
    def show_setup_dialog(self):
        """Toon setup dialoog"""
        dialog = SetupDialog(self.root, self.pm.db_path, self.on_setup_complete)
        dialog.show()
    
    def on_login_success(self):
        """Callback bij succesvolle login"""
        self.setup_main_ui()
    
    def on_setup_complete(self):
        """Callback bij voltooide setup"""
        self.setup_main_ui()
    
    def setup_main_ui(self):
        """Stel de hoofd UI in"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Update window title
        db_name = os.path.basename(self.pm.db_path)
        self.root.title(f"SavePassword v1.2.0 - {db_name}")
        
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Setup UI components
        self.setup_top_bar(main_container)
        self.setup_content_area(main_container)
        self.setup_status_bar(main_container)
        
        # Load initial data
        self.refresh_ui()
    
    def setup_top_bar(self, parent):
        """Stel de top bar in met knoppen"""
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Action buttons
        buttons = [
            ("🔍 All", self.show_all_passwords, "#4CAF50"),
            ("➕ Add", self.show_add_dialog, "#2196F3"),
            ("🔑 Generate", self.show_generator_dialog, "#FF9800"),
            ("📁 Categories", self.manage_categories, "#9C27B0"),
            ("📤 Export", self.export_passwords, "#607D8B"),
            ("🔄 Refresh", self.refresh_ui, "#009688"),
            ("⚙️ Settings", self.show_settings, "#795548"),
            ("🔄 Switch DB", self.switch_database, "#FF5722")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                top_frame, text=text, command=command,
                bg=color, fg="white", font=('Arial', 9, 'bold'),
                relief="raised", bd=2, padx=10, pady=5
            )
            btn.pack(side=tk.LEFT, padx=2)
            
            # Add hover effects
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self.theme_manager.darken_color(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
    
    def setup_content_area(self, parent):
        """Stel het hoofd content gebied in"""
        content_frame = ttk.Frame(parent)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure grid
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Category explorer (left)
        self.category_explorer = CategoryExplorer(content_frame, self.on_category_selected)
        self.category_explorer.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Password list (right)
        self.password_list = PasswordList(content_frame, self.on_password_action)
        self.password_list.grid(row=0, column=1, sticky="nsew")
    
    def setup_status_bar(self, parent):
        """Stel de status bar in"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT)
        
        self.stats_var = tk.StringVar(value="Passwords: 0 | Categories: 0")
        stats_label = ttk.Label(status_frame, textvariable=self.stats_var)
        stats_label.pack(side=tk.RIGHT)
    
    def refresh_ui(self):
        """Vernieuw de UI met huidige data"""
        if not self.pm:
            return
        
        # Update categories
        categories = self.pm.get_all_categories_flat()
        self.category_explorer.update_categories(categories)
        
        # Update passwords
        passwords = self.pm.get_all_passwords()
        self.password_list.update_passwords(passwords)
        
        # Update statistics
        self.update_statistics()
        
        self.status_var.set("Ready")
    
    def update_statistics(self):
        """Update statistieken"""
        if not self.pm:
            return
        
        passwords = self.pm.get_all_passwords()
        categories = self.pm.get_all_categories_flat()
        
        self.stats_var.set(f"Passwords: {len(passwords)} | Categories: {len(categories)}")
    
    def on_category_selected(self, category_name):
        """Callback wanneer categorie is geselecteerd"""
        self.password_list.filter_by_category(category_name)
    
    def on_password_action(self, action, password_id):
        """Callback voor wachtwoord acties"""
        if action == "view":
            self.view_password(password_id)
        elif action == "edit":
            self.edit_password(password_id)
        elif action == "copy_password":
            self.copy_password(password_id)
        elif action == "copy_username":
            self.copy_username(password_id)
        elif action == "open_website":
            self.open_website(password_id)
        elif action == "delete":
            self.delete_password(password_id)
    
    # Dialog methods
    def show_all_passwords(self):
        self.password_list.clear_filters()
    
    def show_add_dialog(self):
        dialog = AddPasswordDialog(self.root, self.pm, self.on_password_saved)
        dialog.show()
    
    def show_generator_dialog(self):
        dialog = PasswordGeneratorDialog(self.root, self.pm)
        dialog.show()
    
    def manage_categories(self):
        dialog = CategoryManagerDialog(self.root, self.pm, self.on_categories_updated)
        dialog.show()
    
    def show_settings(self):
        dialog = SettingsDialog(self.root, self.pm, self.on_settings_updated)
        dialog.show()
    
    def view_password(self, password_id):
        dialog = ViewPasswordDialog(self.root, self.pm, password_id)
        dialog.show()
    
    def edit_password(self, password_id):
        dialog = EditPasswordDialog(self.root, self.pm, password_id, self.on_password_saved)
        dialog.show()
    
    def copy_password(self, password_id):
        # Implementation for copying password
        pass
    
    def copy_username(self, password_id):
        # Implementation for copying username
        pass
    
    def open_website(self, password_id):
        # Implementation for opening website
        pass
    
    def delete_password(self, password_id):
        # Implementation for deleting password
        pass
    
    def export_passwords(self):
        dialog = ExportDialog(self.root, self.pm)
        dialog.show()
    
    def switch_database(self):
        if tk.messagebox.askyesno("Switch Database", "Are you sure you want to switch databases?"):
            for widget in self.root.winfo_children():
                widget.destroy()
            self.pm = None
            self.show_database_selection()
    
    def on_password_saved(self):
        """Callback wanneer wachtwoord is opgeslagen"""
        self.refresh_ui()
        self.status_var.set("Password saved successfully")
    
    def on_categories_updated(self):
        """Callback wanneer categorieën zijn bijgewerkt"""
        self.refresh_ui()
        self.status_var.set("Categories updated")
    
    def on_settings_updated(self):
        """Callback wanneer instellingen zijn bijgewerkt"""
        theme = self.settings_manager.get('theme', 'light')
        self.theme_manager.apply_theme(self.root, theme)
        self.status_var.set("Settings updated")