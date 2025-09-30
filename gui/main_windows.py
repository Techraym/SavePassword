"""
Hoofdvenster voor SavePassword GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os

from core.password_manager import PasswordManager
from gui.dialogs import DatabaseSelectionDialog, LoginDialog, SetupDialog, AddPasswordDialog
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
        self.root.minsize(1000, 600)
        
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
        dialog = LoginDialog(self.root, self.pm, self.on_login_success)
        dialog.show()
    
    def show_setup_dialog(self):
        """Toon setup dialoog"""
        dialog = SetupDialog(self.root, self.pm, self.on_setup_complete)
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
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Setup UI components
        self.setup_top_bar(main_container)
        self.setup_content_area(main_container)
        self.setup_status_bar(main_container)
        
        # Load initial data
        self.refresh_ui()
    
    def setup_top_bar(self, parent):
        """Stel de top bar in met knoppen"""
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Action buttons
        buttons = [
            ("🔍 All", self.show_all_passwords, "#4CAF50"),
            ("➕ Add Password", self.show_add_dialog, "#2196F3"),
            ("🔄 Refresh", self.refresh_ui, "#009688"),
            ("⚙️ Settings", self.show_settings, "#795548"),
            ("🔄 Switch DB", self.switch_database, "#FF5722")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                top_frame, text=text, command=command,
                bg=color, fg="white", font=('Arial', 10, 'bold'),
                relief="raised", bd=2, padx=15, pady=8
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            # Add hover effects
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self.darken_color(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
    
    def darken_color(self, color, factor=0.8):
        """Darken a color for hover effect"""
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
    
    def setup_content_area(self, parent):
        """Stel het hoofd content gebied in"""
        # Create a paned window for resizable split view
        paned_window = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Category explorer (left pane)
        category_frame = ttk.Frame(paned_window)
        paned_window.add(category_frame, weight=1)
        
        self.category_explorer = CategoryExplorer(category_frame, self.on_category_selected)
        self.category_explorer.pack(fill=tk.BOTH, expand=True)
        
        # Password list (right pane)  
        password_frame = ttk.Frame(paned_window)
        paned_window.add(password_frame, weight=3)
        
        self.password_list = PasswordList(password_frame, self.on_password_action)
        self.password_list.pack(fill=tk.BOTH, expand=True)
    
    def setup_status_bar(self, parent):
        """Stel de status bar in"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_var = tk.StringVar(value="Ready - Welcome to SavePassword!")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT)
        
        self.stats_var = tk.StringVar(value="Passwords: 0 | Categories: 0")
        stats_label = ttk.Label(status_frame, textvariable=self.stats_var)
        stats_label.pack(side=tk.RIGHT)
    
    def refresh_ui(self):
        """Vernieuw de UI met huidige data"""
        if not self.pm:
            return
        
        try:
            # Update categories
            categories = self.pm.get_all_categories_flat()
            self.category_explorer.update_categories(categories)
            
            # Update passwords - gebruik sample data als database leeg is
            passwords = self.pm.get_all_passwords()
            if not passwords:
                # Voeg enkele voorbeeld wachtwoorden toe als database leeg is
                self.add_sample_passwords()
                passwords = self.pm.get_all_passwords()
            
            self.password_list.update_passwords(passwords)
            
            # Update statistics
            self.update_statistics()
            
            self.status_var.set("Application ready")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
    
    def add_sample_passwords(self):
        """Voeg voorbeeld wachtwoorden toe voor demonstratie"""
        sample_data = [
            {
                'title': 'Gmail Account',
                'username': 'user@gmail.com', 
                'password': 'MySecurePassword123!',
                'website': 'https://gmail.com',
                'notes': 'Personal email account',
                'category_id': None
            },
            {
                'title': 'Facebook',
                'username': 'myusername',
                'password': 'FacebookPass456!',
                'website': 'https://facebook.com',
                'notes': 'Social media account',
                'category_id': None
            },
            {
                'title': 'Online Banking',
                'username': '123456789',
                'password': 'Banking789!',
                'website': 'https://mybank.com',
                'notes': 'Online banking portal',
                'category_id': None
            }
        ]
        
        for data in sample_data:
            self.pm.add_password(
                data['title'], data['username'], data['password'],
                data['website'], data['notes'], data['category_id']
            )
    
    def update_statistics(self):
        """Update statistieken"""
        if not self.pm:
            return
        
        try:
            passwords = self.pm.get_all_passwords()
            categories = self.pm.get_all_categories_flat()
            
            password_count = len(passwords)
            category_count = len(categories)
            
            self.stats_var.set(f"Passwords: {password_count} | Categories: {category_count}")
        except Exception as e:
            self.stats_var.set("Statistics: N/A")
    
    def on_category_selected(self, category_name):
        """Callback wanneer categorie is geselecteerd"""
        self.password_list.filter_by_category(category_name)
        self.status_var.set(f"Filtered by category: {category_name}")
    
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
        """Show all passwords"""
        self.password_list.clear_filters()
        self.status_var.set("Showing all passwords")
    
    def show_add_dialog(self):
        """Show add password dialog"""
        dialog = AddPasswordDialog(self.root, self.pm, self.on_password_saved)
        dialog.show()
    
    def show_settings(self):
        """Show settings dialog"""
        messagebox.showinfo("Settings", "Settings functionality will be implemented in future version")
        self.status_var.set("Settings dialog opened")
    
    def view_password(self, password_id):
        """View password details"""
        try:
            password = self.pm.get_password_by_id(password_id)
            if password:
                details = f"""
Title: {password['title']}
Username: {password['username'] or 'N/A'}
Password: {password['password']}
Website: {password['website'] or 'N/A'}
Category: {password['category'] or 'Uncategorized'}
Notes: {password['notes'] or 'N/A'}
                """.strip()
                
                messagebox.showinfo("Password Details", details)
                self.status_var.set(f"Viewed password: {password['title']}")
            else:
                messagebox.showerror("Error", "Password not found")
        except Exception as e:
            messagebox.showerror("Error", f"Could not view password: {str(e)}")
    
    def edit_password(self, password_id):
        """Edit password"""
        messagebox.showinfo("Edit Password", "Edit functionality will be implemented in future version")
        self.status_var.set("Edit password dialog opened")
    
    def copy_password(self, password_id):
        """Copy password to clipboard"""
        try:
            password = self.pm.get_password_by_id(password_id)
            if password:
                self.root.clipboard_clear()
                self.root.clipboard_append(password['password'])
                self.status_var.set("Password copied to clipboard")
            else:
                messagebox.showerror("Error", "Password not found")
        except Exception as e:
            messagebox.showerror("Error", f"Could not copy password: {str(e)}")
    
    def copy_username(self, password_id):
        """Copy username to clipboard"""
        try:
            password = self.pm.get_password_by_id(password_id)
            if password and password['username']:
                self.root.clipboard_clear()
                self.root.clipboard_append(password['username'])
                self.status_var.set("Username copied to clipboard")
            else:
                messagebox.showwarning("Warning", "No username available to copy")
        except Exception as e:
            messagebox.showerror("Error", f"Could not copy username: {str(e)}")
    
    def open_website(self, password_id):
        """Open website in browser"""
        try:
            password = self.pm.get_password_by_id(password_id)
            if password and password['website']:
                import webbrowser
                url = password['website']
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                webbrowser.open(url)
                self.status_var.set("Website opened in browser")
            else:
                messagebox.showwarning("Warning", "No website URL available")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open website: {str(e)}")
    
    def delete_password(self, password_id):
        """Delete password"""
        try:
            password = self.pm.get_password_by_id(password_id)
            if password:
                if messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete '{password['title']}'?"):
                    if self.pm.delete_password(password_id):
                        self.refresh_ui()
                        self.status_var.set("Password deleted successfully")
                    else:
                        messagebox.showerror("Error", "Failed to delete password")
            else:
                messagebox.showerror("Error", "Password not found")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete password: {str(e)}")
    
    def switch_database(self):
        """Switch to different database"""
        if messagebox.askyesno("Switch Database", 
                             "Are you sure you want to switch databases?\nCurrent data will be saved."):
            for widget in self.root.winfo_children():
                widget.destroy()
            self.pm = None
            self.show_database_selection()
    
    def on_password_saved(self):
        """Callback wanneer wachtwoord is opgeslagen"""
        self.refresh_ui()
        self.status_var.set("Password saved successfully")