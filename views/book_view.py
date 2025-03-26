import tkinter as tk
from models.database import database

class BookView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = tk.Label(self, text="📚 Buchübersicht", font=("Arial", 14, "bold"))
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.load_books()

    def load_books(self):
        """Lädt die Bücher aus der Datenbank und zeigt sie an."""
        books = database.get_all_books()
        self.listbox.delete(0, tk.END)
        for book in books:
            self.listbox.insert(tk.END, f"{book['title']} ({book['publishedYear'].year})")

