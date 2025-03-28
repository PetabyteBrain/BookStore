# digital_library/views/book_view.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.controller import LibraryController

class BookView(tk.Frame):
    def __init__(self, parent, db_connection):
        """
        Book view for managing and browsing books
        
        Args:
            parent (tk.Notebook): Parent notebook
            db_connection (DatabaseConnection): Database connection
        """
        super().__init__(parent)
        self.db_connection = db_connection
        self.controller = LibraryController(db_connection)
        
        # Layout
        self.create_search_section()
        self.create_book_table()
        self.create_action_buttons()
    
    def create_search_section(self):
        """Create search input and button"""
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10, padx=10, fill='x')
        
        tk.Label(search_frame, text="Search Books:").pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_button = tk.Button(search_frame, text="Search", command=self.search_books)
        search_button.pack(side=tk.LEFT)
    
    def create_book_table(self):
        """Create treeview to display books"""
        columns = ('Title', 'Author', 'ISBN', 'Year', 'Price', 'Categories')
        self.book_table = ttk.Treeview(self, columns=columns, show='headings')
        
        for col in columns:
            self.book_table.heading(col, text=col)
            self.book_table.column(col, width=100)
        
        self.book_table.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Load initial books
        self.load_books()
    
    def create_action_buttons(self):
        """Create buttons for book management"""
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        buttons = [
            ("Add Book", self.add_book),
            ("Edit Book", self.edit_book),
            ("Delete Book", self.delete_book),
            ("Refresh", self.load_books)
        ]
        
        for label, command in buttons:
            tk.Button(button_frame, text=label, command=command).pack(side=tk.LEFT, padx=5)
    
    def load_books(self):
        """Load books from database"""
        # Clear existing items
        for item in self.book_table.get_children():
            self.book_table.delete(item)
        
        # Fetch books
        books = self.db_connection.books.find({})
        
        for book in books:
            # Convert categories to strings if they are ObjectId
            categories = book.get('categories', [])
            categories_str = ', '.join(str(cat) for cat in categories) if categories else ''
            
            self.book_table.insert('', 'end', values=(
                book.get('title', ''),
                book.get('author', ''),
                book.get('isbn', ''),
                book.get('publishedYear', ''),
                book.get('price', ''),
                categories_str
            ))
    
    def search_books(self):
        """Search books based on user input"""
        search_term = self.search_var.get().strip()
        
        if not search_term:
            self.load_books()
            return
        
        # Perform search
        query = {
            '$or': [
                {'title': {'$regex': search_term, '$options': 'i'}},
                {'author': {'$regex': search_term, '$options': 'i'}},
                {'isbn': {'$regex': search_term, '$options': 'i'}}
            ]
        }
        
        # Clear existing items
        for item in self.book_table.get_children():
            self.book_table.delete(item)
        
        # Fetch and display results
        books = self.controller.search_books(query)
        
        for book in books:
            # Convert categories to strings if they are ObjectId
            categories = book.get('categories', [])
            categories_str = ', '.join(str(cat) for cat in categories) if categories else ''
            
            self.book_table.insert('', 'end', values=(
                book.get('title', ''),
                book.get('author', ''),
                book.get('isbn', ''),
                book.get('publishedYear', ''),
                book.get('price', ''),
                categories_str
            ))
    
    def add_book(self):
        """Open dialog to add a new book"""
        add_window = tk.Toplevel(self)
        add_window.title("Add New Book")
        add_window.geometry("400x500")
        
        # Input fields
        fields = [
            ("Title", "title"),
            ("Author", "author"),
            ("ISBN", "isbn"),
            ("Published Year", "published_year"),
            ("Price", "price"),
            ("Categories", "categories"),
            ("Description", "description"),
            ("Imprint", "imprint")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(add_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            entries[key] = tk.Entry(add_window, width=30)
            entries[key].grid(row=i, column=1, padx=10, pady=5)
        
        def submit():
            book_data = {key: entry.get() for key, entry in entries.items()}
            
            # Convert numeric fields
            book_data['published_year'] = int(book_data['published_year'])
            book_data['price'] = float(book_data['price'])
            book_data['categories'] = book_data['categories'].split(',') if book_data['categories'] else []
            
            result = self.controller.add_book(book_data)
            
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                add_window.destroy()
                self.load_books()
            else:
                messagebox.showerror("Error", result['message'])
        
        tk.Button(add_window, text="Submit", command=submit).grid(row=len(fields), column=0, columnspan=2, pady=10)
    
    def edit_book(self):
        """Edit selected book"""
        selected_item = self.book_table.selection()
        
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a book to edit")
            return
        
        # Get the book details from the selected row
        book_details = self.book_table.item(selected_item[0])['values']
        
        # Open edit window
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Book")
        edit_window.geometry("400x500")
        
        # Helper function to extract year from datetime string
        def extract_year(date_str):
            try:
                # Try parsing different datetime formats
                import datetime
                
                # Try parsing full datetime
                if isinstance(date_str, str) and ' ' in date_str:
                    return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').year
                
                # If it's already a year, return it
                return int(date_str)
            except (ValueError, TypeError):
                # Default to current year if parsing fails
                return datetime.datetime.now().year
        
        # Input fields with pre-filled values
        fields = [
            ("Title", "title", book_details[0]),
            ("Author", "author", book_details[1]),
            ("ISBN", "isbn", book_details[2]),
            ("Published Year", "published_year", extract_year(book_details[3])),
            ("Price", "price", book_details[4]),
            ("Categories", "categories", book_details[5]),
            ("Description", "description", ""),  # You might want to fetch this from database
            ("Imprint", "imprint", "")  # You might want to fetch this from database
        ]
        
        entries = {}
        for i, (label, key, default_value) in enumerate(fields):
            tk.Label(edit_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            entries[key] = tk.Entry(edit_window, width=30)
            entries[key].insert(0, str(default_value))
            entries[key].grid(row=i, column=1, padx=10, pady=5)
        
        def submit():
            book_data = {key: entry.get() for key, entry in entries.items()}
            
            try:
                # Convert numeric fields
                book_data['published_year'] = int(book_data['published_year'])
                book_data['price'] = float(book_data['price'])
                book_data['categories'] = book_data['categories'].split(',') if book_data['categories'] else []
                
                # Original ISBN for identifying the book to update
                original_isbn = book_details[2]
                
                result = self.controller.edit_book(original_isbn, book_data)
                
                if result['success']:
                    messagebox.showinfo("Success", result['message'])
                    edit_window.destroy()
                    self.load_books()
                else:
                    messagebox.showerror("Error", result['message'])
            
            except ValueError as e:
                messagebox.showerror("Input Error", f"Invalid input: {str(e)}")
        
        tk.Button(edit_window, text="Submit", command=submit).grid(row=len(fields), column=0, columnspan=2, pady=10)
    
    def delete_book(self):
        """Delete selected book"""
        selected_item = self.book_table.selection()

        if not selected_item:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return

        # Get the book details from the selected row
        book_details = self.book_table.item(selected_item[0])['values']

        # Print out the exact book details for debugging
        print("Book details to delete:", book_details)

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", 
            f"Are you sure you want to delete the book:\n\nTitle: {book_details[0]}\nAuthor: {book_details[1]}\nISBN: {book_details[2]}")

        if confirm:
            try:
                # Find the book in the database using the ISBN (assuming it's the third column)
                result = self.controller.delete_book(book_details[2])

                if result['success']:
                    messagebox.showinfo("Success", result['message'])
                    self.load_books()  # Refresh the book table
                else:
                    messagebox.showerror("Error", result['message'])

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")