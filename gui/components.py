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
        
        # Build category tree
        category_dict = {}
        for category in categories:
            cat_id = category['id']
            parent_id = category['parent_id']
            name = category['name']
            
            if parent_id is None:
                # Root category
                item_id = self.tree.insert('', 'end', text=name, values=(cat_id,))
            else:
                # Child category
                parent_item = self.find_tree_item(self.tree, parent_id)
                if parent_item:
                    item_id = self.tree.insert(parent_item, 'end', text=name, values=(cat_id,))
                else:
                    # If parent not found, add as root
                    item_id = self.tree.insert('', 'end', text=name, values=(cat_id,))
            
            category_dict[cat_id] = item_id
        
        # Auto-expand first level
        for child in self.tree.get_children():
            self.tree.item(child, open=True)
    
    def find_tree_item(self, tree, category_id):
        """Find tree item by category ID"""
        for item in tree.get_children():
            if tree.item(item)['values'] and tree.item(item)['values'][0] == category_id:
                return item
            # Check children recursively
            child_item = self.find_tree_item_in_children(tree, item, category_id)
            if child_item:
                return child_item
        return None
    
    def find_tree_item_in_children(self, tree, parent_item, category_id):
        """Find tree item in children recursively"""
        for item in tree.get_children(parent_item):
            if tree.item(item)['values'] and tree.item(item)['values'][0] == category_id:
                return item
            child_item = self.find_tree_item_in_children(tree, item, category_id)
            if child_item:
                return child_item
        return None
    
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
            # Show all categories
            for item in self.tree.get_children():
                self.tree.item(item, tags=())
                self.show_children(item)
            return
        
        # Hide all first
        for item in self.tree.get_children():
            self.tree.item(item, tags=('hidden',))
            self.hide_children(item)
        
        # Show matching categories and their parents
        for item in self.tree.get_children():
            if self.search_item(item, search_term):
                self.show_item_and_parents(item)
    
    def search_item(self, item, search_term):
        """Check if item matches search term"""
        text = self.tree.item(item, 'text').lower()
        if search_term in text:
            return True
        
        # Check children
        for child in self.tree.get_children(item):
            if self.search_item(child, search_term):
                return True
        
        return False
    
    def show_item_and_parents(self, item):
        """Show item and all its parents"""
        self.tree.item(item, tags=())
        parent = self.tree.parent(item)
        if parent:
            self.show_item_and_parents(parent)
    
    def show_children(self, item):
        """Show all children of an item"""
        for child in self.tree.get_children(item):
            self.tree.item(child, tags=())
            self.show_children(child)
    
    def hide_children(self, item):
        """Hide all children of an item"""
        for child in self.tree.get_children(item):
            self.tree.item(child, tags=('hidden',))
            self.hide_children(child)
    
    def refresh(self):
        """Refresh categories"""
        # This would typically call a callback to refresh from database
        pass
    
    def expand_all(self):
        """Expand all categories"""
        for item in self.tree.get_children():
            self.tree.item(item, open=True)
            self.expand_children(item)
    
    def expand_children(self, item):
        """Expand all children of an item"""
        for child in self.tree.get_children(item):
            self.tree.item(child, open=True)
            self.expand_children(child)
    
    def collapse_all(self):
        """Collapse all categories"""
        for item in self.tree.get_children():
            self.tree.item(item, open=False)
            self.collapse_children(item)
    
    def collapse_children(self, item):
        """Collapse all children of an item"""
        for child in self.tree.get_children(item):
            self.tree.item(child, open=False)
            self.collapse_children(child)

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
        frame = ttk.LabelFrame(self.parent, text="Passwords")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Search and filter
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar()
        filter_entry = ttk.Entry(filter_frame, textvariable=self.filter_var, width=30)
        filter_entry.pack(side=tk.LEFT, padx=5)
        filter_entry.bind('<KeyRelease>', self.on_filter)
        
        ttk.Button(filter_frame, text="Clear", command=self.clear_filters).pack(side=tk.LEFT, padx=5)
        
        # Password list
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview with columns
        columns = ('title', 'username', 'website', 'category')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Define headings
        self.tree.heading('title', text='Title')
        self.tree.heading('username', text='Username')
        self.tree.heading('website', text='Website')
        self.tree.heading('category', text='Category')
        
        # Configure column widths
        self.tree.column('title', width=200)
        self.tree.column('username', width=150)
        self.tree.column('website', width=150)
        self.tree.column('category', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
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
                    filter_text in (pwd['username'] or '').lower() or
                    filter_text in (pwd['website'] or '').lower() or
                    filter_text in (pwd['category'] or '').lower())
            ]
        
        # Apply category filter
        if self.current_filter and self.current_filter != "All":
            self.filtered_passwords = [
                pwd for pwd in self.filtered_passwords
                if pwd['category'] == self.current_filter
            ]
        
        self.refresh_tree()
    
    def refresh_tree(self):
        """Refresh the treeview with filtered passwords"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add filtered passwords
        for pwd in self.filtered_passwords:
            self.tree.insert('', 'end', values=(
                pwd['title'],
                pwd['username'] or '',
                pwd['website'] or '',
                pwd['category'] or 'Uncategorized'
            ), tags=(pwd['id'],))
    
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
        self.current_filter = category_name
        self.apply_filters()
    
    def on_double_click(self, event):
        """Handle double click on password"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            password_id = self.tree.item(item, 'tags')[0]
            self.action_callback("view", password_id)
    
    def on_right_click(self, event):
        """Handle right click for context menu"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            password_id = self.tree.item(item, 'tags')[0]
            self.show_context_menu(event, password_id)
    
    def show_context_menu(self, event, password_id):
        """Show context menu for password actions"""
        menu = tk.Menu(self.parent, tearoff=0)
        menu.add_command(label="View Details", command=lambda: self.action_callback("view", password_id))
        menu.add_command(label="Edit", command=lambda: self.action_callback("edit", password_id))
        menu.add_separator()
        menu.add_command(label="Copy Username", command=lambda: self.action_callback("copy_username", password_id))
        menu.add_command(label="Copy Password", command=lambda: self.action_callback("copy_password", password_id))
        menu.add_separator()
        menu.add_command(label="Open Website", command=lambda: self.action_callback("open_website", password_id))
        menu.add_separator()
        menu.add_command(label="Delete", command=lambda: self.action_callback("delete", password_id))
        
        menu.tk_popup(event.x_root, event.y_root)