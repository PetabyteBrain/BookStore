# digital_library/views/review_view.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.controller import LibraryController

class ReviewView(tk.Frame):
    def __init__(self, parent, db_connection):
        """
        Review view for managing book reviews
        
        Args:
            parent (tk.Notebook): Parent notebook
            db_connection (DatabaseConnection): Database connection
        """
        super().__init__(parent)
        self.db_connection = db_connection
        self.controller = LibraryController(db_connection)
        
        # Layout
        self.create_search_section()
        self.create_review_table()
        self.create_action_buttons()
    
    def create_search_section(self):
        """Create search input and section for finding reviews"""
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10, padx=10, fill='x')
        
        tk.Label(search_frame, text="Search Reviews:").pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_button = tk.Button(search_frame, text="Search", command=self.search_reviews)
        search_button.pack(side=tk.LEFT)
    
    def create_review_table(self):
        """Create treeview to display reviews"""
        columns = ('Book', 'User', 'Rating', 'Review Text', 'Date')
        self.review_table = ttk.Treeview(self, columns=columns, show='headings')
        
        for col in columns:
            self.review_table.heading(col, text=col)
            self.review_table.column(col, width=150)
        
        self.review_table.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Load initial reviews
        self.load_reviews()
    
    def create_action_buttons(self):
        """Create buttons for review management"""
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        buttons = [
            ("Add Review", self.add_review),
            ("Edit Review", self.edit_review),
            ("Delete Review", self.delete_review),
            ("Refresh", self.load_reviews)
        ]
        
        for label, command in buttons:
            tk.Button(button_frame, text=label, command=command).pack(side=tk.LEFT, padx=5)
    
    def load_reviews(self):
        """Load reviews from database"""
        # Clear existing items
        for item in self.review_table.get_children():
            self.review_table.delete(item)
        
        # Fetch reviews with book and user details
        reviews = list(self.db_connection.reviews.aggregate([
            {
                '$lookup': {
                    'from': 'books',
                    'localField': 'book_id',
                    'foreignField': '_id',
                    'as': 'book_details'
                }
            },
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'user_id',
                    'foreignField': '_id',
                    'as': 'user_details'
                }
            }
        ]))
        
        for review in reviews:
            book = review['book_details'][0] if review['book_details'] else {'title': 'Unknown Book'}
            user = review['user_details'][0] if review['user_details'] else {'username': 'Unknown User'}
            
            self.review_table.insert('', 'end', values=(
                book.get('title', 'Unknown'),
                user.get('username', 'Unknown'),
                review.get('rating', 'N/A'),
                review.get('review_text', ''),
                review.get('review_date', 'N/A')
            ))
    
    def search_reviews(self):
        """Search reviews based on user input"""
        search_term = self.search_var.get().strip()
        
        if not search_term:
            self.load_reviews()
            return
        
        # Clear existing items
        for item in self.review_table.get_children():
            self.review_table.delete(item)
        
        # Perform search
        reviews = list(self.db_connection.reviews.aggregate([
            {
                '$lookup': {
                    'from': 'books',
                    'localField': 'book_id',
                    'foreignField': '_id',
                    'as': 'book_details'
                }
            },
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
                        {'book_details.title': {'$regex': search_term, '$options': 'i'}},
                        {'user_details.username': {'$regex': search_term, '$options': 'i'}},
                        {'review_text': {'$regex': search_term, '$options': 'i'}}
                    ]
                }
            }
        ]))
        
        for review in reviews:
            book = review['book_details'][0] if review['book_details'] else {'title': 'Unknown Book'}
            user = review['user_details'][0] if review['user_details'] else {'username': 'Unknown User'}
            
            self.review_table.insert('', 'end', values=(
                book.get('title', 'Unknown'),
                user.get('username', 'Unknown'),
                review.get('rating', 'N/A'),
                review.get('review_text', ''),
                review.get('review_date', 'N/A')
            ))
    
    def add_review(self):
        """Add a new review"""
        review_window = tk.Toplevel(self)
        review_window.title("Add New Review")
        review_window.geometry("400x500")
        
        # Book selection
        tk.Label(review_window, text="Select Book:").pack()
        books = list(self.db_connection.books.find())
        book_var = tk.StringVar()
        book_dropdown = ttk.Combobox(
            review_window, 
            textvariable=book_var, 
            values=[f"{book['title']} - {book['author']}" for book in books]
        )
        book_dropdown.pack()
        
        # User selection
        tk.Label(review_window, text="Select User:").pack()
        users = list(self.db_connection.users.find())
        user_var = tk.StringVar()
        user_dropdown = ttk.Combobox(
            review_window, 
            textvariable=user_var, 
            values=[user['username'] for user in users]
        )
        user_dropdown.pack()
        
        # Rating selection
        tk.Label(review_window, text="Rating:").pack()
        rating_var = tk.IntVar()
        rating_dropdown = ttk.Combobox(
            review_window, 
            textvariable=rating_var, 
            values=list(range(1, 6))
        )
        rating_dropdown.pack()
        
        # Review text input
        tk.Label(review_window, text="Review Text:").pack()
        review_text = tk.Text(review_window, height=10, width=50)
        review_text.pack()
        
        def submit_review():
            selected_book = book_var.get()
            selected_username = user_var.get()
            rating = rating_var.get()
            text = review_text.get("1.0", tk.END).strip()
            
            if not all([selected_book, selected_username, rating, text]):
                messagebox.showwarning("Warning", "Please fill in all fields")
                return
            
            # Find book and user IDs
            book = self.db_connection.books.find_one({
                'title': selected_book.split(' - ')[0]
            })
            user = self.db_connection.users.find_one({'username': selected_username})
            
            if not book or not user:
                messagebox.showerror("Error", "Book or User not found")
                return
            
            # Create review (you'll need to implement this in the controller)
            review_data = {
                'book_id': book['_id'],
                'user_id': user['_id'],
                'rating': rating,
                'review_text': text,
                'review_date': tk.datetime.now()
            }
            
            try:
                self.db_connection.reviews.insert_one(review_data)
                messagebox.showinfo("Success", "Review added successfully")
                review_window.destroy()
                self.load_reviews()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(review_window, text="Submit Review", command=submit_review).pack(pady=10)
    
    def edit_review(self):
        """Edit selected review"""
        selected_item = self.review_table.selection()
        
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a review to edit")
            return
        
        # Placeholder for review editing functionality
        messagebox.showinfo("Info", "Edit review functionality to be implemented")
    
    def delete_review(self):
        """Delete selected review"""
        selected_item = self.review_table.selection()
        
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a review to delete")
            return
        
        # Placeholder for review deletion functionality
        messagebox.showinfo("Info", "Delete review functionality to be implemented")