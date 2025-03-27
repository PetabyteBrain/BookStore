# digital_library/views/order_view.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.controller import LibraryController

class OrderView(tk.Frame):
    def __init__(self, parent, db_connection):
        """
        Order view for managing and tracking orders
        
        Args:
            parent (tk.Notebook): Parent notebook
            db_connection (DatabaseConnection): Database connection
        """
        super().__init__(parent)
        self.db_connection = db_connection
        self.controller = LibraryController(db_connection)
        
        # Layout
        self.create_search_section()
        self.create_order_table()
        self.create_action_buttons()
    
    def create_search_section(self):
        """Create search input and section for finding orders"""
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10, padx=10, fill='x')
        
        tk.Label(search_frame, text="Search Orders:").pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_button = tk.Button(search_frame, text="Search", command=self.search_orders)
        search_button.pack(side=tk.LEFT)
    
    def create_order_table(self):
        """Create treeview to display orders"""
        columns = ('Order ID', 'User', 'Total Books', 'Total Price', 'Order Date')
        self.order_table = ttk.Treeview(self, columns=columns, show='headings')
        
        for col in columns:
            self.order_table.heading(col, text=col)
            self.order_table.column(col, width=150)
        
        self.order_table.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Load initial orders
        self.load_orders()
    
    def create_action_buttons(self):
        """Create buttons for order management"""
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        buttons = [
            ("Create Order", self.create_order),
            ("View Details", self.view_order_details),
            ("Refresh", self.load_orders)
        ]
        
        for label, command in buttons:
            tk.Button(button_frame, text=label, command=command).pack(side=tk.LEFT, padx=5)
    
    def load_orders(self):
        """Load orders from database"""
        # Clear existing items
        for item in self.order_table.get_children():
            self.order_table.delete(item)
        
        # Fetch orders with user details
        orders = list(self.db_connection.orders.aggregate([
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'user_id',
                    'foreignField': '_id',
                    'as': 'user_details'
                }
            }
        ]))
        
        for order in orders:
            user = order['user_details'][0] if order['user_details'] else {'username': 'Unknown'}
            
            self.order_table.insert('', 'end', values=(
                str(order.get('_id', '')),
                user.get('username', 'Unknown'),
                len(order.get('book_ids', [])),
                f"€{order.get('total_price', 0):.2f}",
                order.get('order_date', 'N/A')
            ))
    
    def search_orders(self):
        """Search orders based on user input"""
        search_term = self.search_var.get().strip()
        
        if not search_term:
            self.load_orders()
            return
        
        # Clear existing items
        for item in self.order_table.get_children():
            self.order_table.delete(item)
        
        # Perform search
        orders = list(self.db_connection.orders.aggregate([
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'user_id',
                    'foreignField': '_id',
                    'as': 'user_details'
                }
            },
            {
                '$match': {
                    '$or': [
                        {'user_details.username': {'$regex': search_term, '$options': 'i'}},
                        {'_id': str(search_term)}
                    ]
                }
            }
        ]))
        
        for order in orders:
            user = order['user_details'][0] if order['user_details'] else {'username': 'Unknown'}
            
            self.order_table.insert('', 'end', values=(
                str(order.get('_id', '')),
                user.get('username', 'Unknown'),
                len(order.get('book_ids', [])),
                f"€{order.get('total_price', 0):.2f}",
                order.get('order_date', 'N/A')
            ))
    
    def create_order(self):
        """Create a new order"""
        create_order_window = tk.Toplevel(self)
        create_order_window.title("Create New Order")
        create_order_window.geometry("400x500")
        
        # User selection
        tk.Label(create_order_window, text="Select User:").pack()
        users = list(self.db_connection.users.find())
        user_var = tk.StringVar()
        user_dropdown = ttk.Combobox(
            create_order_window, 
            textvariable=user_var, 
            values=[user['username'] for user in users]
        )
        user_dropdown.pack()
        
        # Book selection (multi-select)
        tk.Label(create_order_window, text="Select Books:").pack()
        books = list(self.db_connection.books.find())
        book_listbox = tk.Listbox(create_order_window, selectmode=tk.MULTIPLE)
        for book in books:
            book_listbox.insert(tk.END, f"{book['title']} - {book['author']}")
        book_listbox.pack()
        
        def submit_order():
            selected_username = user_var.get()
            selected_book_indices = book_listbox.curselection()
            
            if not selected_username or not selected_book_indices:
                messagebox.showwarning("Warning", "Please select a user and books")
                return
            
            # Find user ID
            user = self.db_connection.users.find_one({'username': selected_username})
            
            # Get selected book IDs
            selected_books = [str(books[i]['_id']) for i in selected_book_indices]
            
            # Create order
            result = self.controller.create_order(str(user['_id']), selected_books)
            
            if result['success']:
                messagebox.showinfo("Success", f"Order created. Total price: {result['total_price']}")
                create_order_window.destroy()
                self.load_orders()
            else:
                messagebox.showerror("Error", result['message'])
        
        tk.Button(create_order_window, text="Create Order", command=submit_order).pack(pady=10)
    
    def view_order_details(self):
        """View details of selected order"""
        selected_item = self.order_table.selection()
        
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an order to view")
            return
        
        # Get order details
        order_id = self.order_table.item(selected_item)['values'][0]
        
        details_window = tk.Toplevel(self)
        details_window.title(f"Order Details - {order_id}")
        details_window.geometry("600x400")
        
        # Fetch order and book details
        order = self.db_connection.orders.find_one({'_id': order_id})
        
        if not order:
            messagebox.showerror("Error", "Order not found")
            details_window.destroy()
            return
        
        details_text = tk.Text(details_window)
        details_text.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Add order and book details to text widget
        details_text.insert(tk.END, f"Order ID: {order_id}\n")
        details_text.insert(tk.END, f"Total Price: €{order.get('total_price', 0):.2f}\n")
        details_text.insert(tk.END, f"Order Date: {order.get('order_date', 'N/A')}\n\n")
        
        details_text.insert(tk.END, "Books in this Order:\n")
        for book_id in order.get('book_ids', []):
            book = self.db_connection.books.find_one({'_id': book_id})
            if book:
                details_text.insert(tk.END, f"- {book['title']} by {book['author']} (€{book['price']})\n")
        
        details_text.config(state=tk.DISABLED)