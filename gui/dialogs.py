"""
Dialog windows for SavePassword
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import webbrowser

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
        self.dialog.geometry("400x350")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
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
                entry = ttk.Entry(self.dialog, show="*")
            elif field_name == "notes":
                entry = tk.Text(self.dialog, height=4, width=40)
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
        import random
        import string
        
        length = 16
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(characters) for i in range(length))
        self.entries['password'].delete(0, tk.END)
        self.entries['password'].insert(0, password)

# Add other dialog classes as needed...