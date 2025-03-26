# digital_library/views/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from views.book_view import BookView
from views.user_view import UserView
from views.order_view import OrderView
from views.review_view import ReviewView

class DigitalLibraryApp:
    def __init__(self, root, db_connection):
        """
        Main application window for Digital Library
        
        Args:
            root (tk.Tk): Root Tkinter window
            db_connection (DatabaseConnection): Database connection
        """
        self.root = root
        self.db_connection = db_connection
        
        # Configure root window
        self.root.title("Digital Library Management System")
        self.root.geometry("1024x768")
        
        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create views
        self.create_views()
        
        # Create menu bar
        self.create_menu()
    
    def create_views(self):
        """Create individual views for the notebook"""
        views = [
            ("Books", BookView),
            ("Users", UserView),
            ("Orders", OrderView),
            ("Reviews", ReviewView)
        ]
        
        for title, ViewClass in views:
            view = ViewClass(self.notebook, self.db_connection)
            self.notebook.add(view, text=title)
    
    def create_menu(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def show_about(self):
        """Display about dialog"""
        messagebox.showinfo(
            "About Digital Library", 
            "Digital Library Management System\n\n"
            "Version 1.0\n"
            "Developed by Jonas Raemy & Spyros Catéchis\n\n"
            "A comprehensive library management application\n"
            "powered by Python, Tkinter, and MongoDB."
        )