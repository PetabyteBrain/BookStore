# digital_library/views/user_view.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.controller import LibraryController

class UserView(tk.Frame):
    def __init__(self, parent, db_connection):
        """
        User view for managing user accounts
        
        Args:
            parent (tk.Notebook): Parent notebook
            db_connection (DatabaseConnection): Database connection
        """
        super().__init__(parent)
        self.db_connection = db_connection
        self.controller = LibraryController(db_connection)
        
        # Layout
        self.create_user_section()
        self.create_user_table()
        self.create_action_buttons()
    
    def create_user_section(self):
        """Create search input and section for finding users"""
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10, padx=10, fill='x')
        
        tk.Label(search_frame, text="Search Users:").pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_button = tk.Button(search_frame, text="Search", command=self.search_users)
        search_button.pack(side=tk.LEFT)
    
    def create_user_table(self):
        """Create treeview to display users"""
        columns = ('Username', 'Email', 'Registration Date', 'Total Orders')
        self.user_table = ttk.Treeview(self, columns=columns, show='headings')
        
        for col in columns:
            self.user_table.heading(col, text=col)
            self.user_table.column(col, width=150)
        
        self.user_table.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Load initial users
        self.load_users()
    
    def create_action_buttons(self):
        """Create buttons for user management"""
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        buttons = [
            ("Register User", self.register_user),
            ("Edit User", self.edit_user),
            ("Delete User", self.delete_user),
            ("Refresh", self.load_users)
        ]
        
        for label, command in buttons:
            tk.Button(button_frame, text=label, command=command).pack(side=tk.LEFT, padx=5)
    
    def load_users(self):
        """Load users from database"""
        # Clear existing items
        for item in self.user_table.get_children():
            self.user_table.delete(item)
        
        # Fetch users (implementation depends on your actual controller method)
        users = self.db_connection.users.find({})
        
        for user in users:
            # Calculate total orders for the user
            total_orders = self.db_connection.orders.count_documents({'user_id': user['_id']})
            
            self.user_table.insert('', 'end', values=(
                user.get('username', ''),
                user.get('email', ''),
                user.get('registration_date', 'N/A'),
                total_orders
            ))
    
    def search_users(self):
        """Search users based on user input"""
        search_term = self.search_var.get().strip()
        
        if not search_term:
            self.load_users()
            return
        
        # Clear existing items
        for item in self.user_table.get_children():
            self.user_table.delete(item)
        
        # Perform search
        query = {
            '$or': [
                {'username': {'$regex': search_term, '$options': 'i'}},
                {'email': {'$regex': search_term, '$options': 'i'}}
            ]
        }
        
        users = list(self.db_connection.users.find(query))
        
        for user in users:
            total_orders = self.db_connection.orders.count_documents({'user_id': user['_id']})
            
            self.user_table.insert('', 'end', values=(
                user.get('username', ''),
                user.get('email', ''),
                user.get('registration_date', 'N/A'),
                total_orders
            ))
    
    def register_user(self):
        """Open dialog to register a new user"""
        register_window = tk.Toplevel(self)
        register_window.title("Register New User")
        register_window.geometry("400x300")
        
        # Input fields
        tk.Label(register_window, text="Username:").pack()
        username_entry = tk.Entry(register_window, width=30)
        username_entry.pack()
        
        tk.Label(register_window, text="Email:").pack()
        email_entry = tk.Entry(register_window, width=30)
        email_entry.pack()
        
        tk.Label(register_window, text="Password:").pack()
        password_entry = tk.Entry(register_window, show="*", width=30)
        password_entry.pack()
        
        def submit():
            username = username_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get()
            
            result = self.controller.register_user(username, email, password)
            
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                register_window.destroy()
                self.load_users()
            else:
                messagebox.showerror("Error", result['message'])
        
        tk.Button(register_window, text="Register", command=submit).pack(pady=10)
    
    def edit_user(self):
        """Edit selected user"""
        selected_item = self.user_table.selection()
        
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to edit")
            return
        
        # Implementation of user editing (to be expanded)
        messagebox.showinfo("Info", "Edit user functionality to be implemented")
    
    def delete_user(self):
        """Delete selected user"""
        selected_item = self.user_table.selection()
        
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        # Implementation of user deletion (to be expanded)
        messagebox.showinfo("Info", "Delete user functionality to be implemented")