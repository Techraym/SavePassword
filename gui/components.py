"""
UI Components for SavePassword
"""

import tkinter as tk
from tkinter import ttk
import webbrowser

class CategoryExplorer:
    """Category explorer tree view"""
    
    def __init__(self, parent, selection_callback):
        self.parent = parent
        self.selection_callback = selection_callback
        self.tree = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the category explorer UI"""
        frame = ttk.LabelFrame(self.parent, text="Categories")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Search box
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        search_entry.bind('<KeyRelease>', self.on_search)
        
        # Treeview for categories
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tree = ttk.Treeview(tree_frame, show='tree', selectmode='browse')
        self.tree.heading('#0', text='Categories', anchor=tk.W)
        
        # Scrollbar for tree
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Refresh", command=self.refresh).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Expand All", command=self.expand_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Collapse All", command=self.collapse_all).pack(side=tk.LEFT, padx=2)
    
    def update_categories(self, categories):
        """Update the category tree with new data"""
        self.tree.delete(*self.tree.get_children())
        
        # Add "All Categories" option
        self.tree.insert('', 'end', text="All Categories", values=("all",))
        
        # Build category tree
        for category in categories:
            cat_id = category['id']
            parent_id = category['parent_id']
            name = category['name']
            
            if parent_id is None:
                # Root category
                item_id = self.tree.insert('', 'end', text=name, values=(cat_id,))
            else:
                # Child category - voor nu toevoegen als root
                item_id = self.tree.insert('', 'end', text=name, values=(cat_id,))
        
        # Auto-expand first level
        for child in self.tree.get_children():
            self.tree.item(child, open=True)
    
    def on_tree_select(self, event):
        """Handle tree selection"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            category_name = self.tree.item(item, 'text')
            self.selection_callback(category_name)
    
    def on_search(self, event):
        """Handle search filter"""
        search_term = self.search_var.get().lower()
        if not search_term:
            return
        
        # Hide non-matching items
        for item in self.tree.get_children():
            text = self.tree.item(item, 'text').lower()
            if search_term in text:
                self.tree.item(item, tags=())
            else:
                self.tree.item(item, tags=('hidden',))
    
    def refresh(self):
        """Refresh categories"""
        pass
    
    def expand_all(self):
        """Expand all categories"""
        for item in self.tree.get_children():
            self.tree.item(item, open=True)
    
    def collapse_all(self):
        """Collapse all categories"""
        for item in self.tree.get_children():
            self.tree.item(item, open=False)
    
    def pack(self, **kwargs):
        """Pack the main frame"""
        pass

class PasswordList:
    """Password list with filtering and actions"""
    
    def __init__(self, parent, action_callback):
        self.parent = parent
        self.action_callback = action_callback
        self.all_passwords = []
        self.filtered_passwords = []
        self.current_filter = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the password list UI"""
        # Create main frame
        self.main_frame = ttk.LabelFrame(self.parent, text="Passwords")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search and filter
        filter_frame = ttk.Frame(self.main_frame)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar()
        filter_entry = ttk.Entry(filter_frame, textvariable=self.filter_var, width=30)
        filter_entry.pack(side=tk.LEFT, padx=5)
        filter_entry.bind('<KeyRelease>', self.on_filter)
        
        ttk.Button(filter_frame, text="Clear", command=self.clear_filters).pack(side=tk.LEFT, padx=5)
        
        # Password list container
        list_container = ttk.Frame(self.main_frame)
        list_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview with columns
        columns = ('title', 'username', 'website', 'category')
        self.tree = ttk.Treeview(list_container, columns=columns, show='headings', selectmode='browse')
        
        # Define headings
        self.tree.heading('title', text='Title')
        self.tree.heading('username', text='Username')
        self.tree.heading('website', text='Website')
        self.tree.heading('category', text='Category')
        
        # Configure column widths
        self.tree.column('title', width=200, minwidth=150)
        self.tree.column('username', width=150, minwidth=100)
        self.tree.column('website', width=150, minwidth=100)
        self.tree.column('category', width=120, minwidth=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-3>', self.on_right_click)
    
    def update_passwords(self, passwords):
        """Update the password list"""
        self.all_passwords = passwords
        self.apply_filters()
    
    def apply_filters(self):
        """Apply current filters to password list"""
        self.filtered_passwords = self.all_passwords.copy()
        
        # Apply text filter
        filter_text = self.filter_var.get().lower()
        if filter_text:
            self.filtered_passwords = [
                pwd for pwd in self.filtered_passwords
                if (filter_text in pwd['title'].lower() or 
                    filter_text in (pwd.get('username', '') or '').lower() or
                    filter_text in (pwd.get('website', '') or '').lower() or
                    filter_text in (pwd.get('category', '') or '').lower())
            ]
        
        # Apply category filter
        if self.current_filter and self.current_filter != "All Categories":
            self.filtered_passwords = [
                pwd for pwd in self.filtered_passwords
                if pwd.get('category', '') == self.current_filter
            ]
        
        self.refresh_tree()
    
    def refresh_tree(self):
        """Refresh the treeview with filtered passwords"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add filtered passwords
        for pwd in self.filtered_passwords:
            self.tree.insert('', 'end', 
                           values=(
                               pwd['title'],
                               pwd.get('username', '') or '',
                               pwd.get('website', '') or '',
                               pwd.get('category', '') or 'Uncategorized'
                           ), 
                           tags=(str(pwd['id']),))
    
    def on_filter(self, event):
        """Handle filter text change"""
        self.apply_filters()
    
    def clear_filters(self):
        """Clear all filters"""
        self.filter_var.set("")
        self.current_filter = None
        self.apply_filters()
    
    def filter_by_category(self, category_name):
        """Filter by category"""
        if category_name == "All Categories":
            self.current_filter = None
        else:
            self.current_filter = category_name
        self.apply_filters()
    
    def on_double_click(self, event):
        """Handle double click on password"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            tags = self.tree.item(item, 'tags')
            if tags:
                password_id = tags[0]
                self.action_callback("view", password_id)
    
    def on_right_click(self, event):
        """Handle right click for context menu"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            tags = self.tree.item(item, 'tags')
            if tags:
                password_id = tags[0]
                self.show_context_menu(event, password_id)
    
    def show_context_menu(self, event, password_id):
        """Show context menu for password actions"""
        menu = tk.Menu(self.parent, tearoff=0)
        menu.add_command(label="View Details", 
                        command=lambda: self.action_callback("view", password_id))
        menu.add_command(label="Edit", 
                        command=lambda: self.action_callback("edit", password_id))
        menu.add_separator()
        menu.add_command(label="Copy Username", 
                        command=lambda: self.action_callback("copy_username", password_id))
        menu.add_command(label="Copy Password", 
                        command=lambda: self.action_callback("copy_password", password_id))
        menu.add_separator()
        menu.add_command(label="Open Website", 
                        command=lambda: self.action_callback("open_website", password_id))
        menu.add_separator()
        menu.add_command(label="Delete", 
                        command=lambda: self.action_callback("delete", password_id))
        
        menu.tk_popup(event.x_root, event.y_root)
    
    def pack(self, **kwargs):
        """Pack the main frame"""
        self.main_frame.pack(**kwargs)