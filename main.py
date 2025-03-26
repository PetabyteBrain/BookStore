import tkinter as tk
from controllers.controller import Controller

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Library")

        self.nav_frame = tk.Frame(self.root)
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)

        self.book_btn = tk.Button(self.nav_frame, text="📚 Bücher", command=self.show_books)
        self.book_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.order_btn = tk.Button(self.nav_frame, text="🛒 Bestellungen", command=self.show_orders)
        self.order_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.view_frame = tk.Frame(self.root)
        self.view_frame.pack(fill=tk.BOTH, expand=True)

        self.controller = Controller(self.view_frame)

        self.show_books()

    def show_books(self):
        self.controller.show_book_view()

    def show_orders(self):
        self.controller.show_order_view()  # Bestellansicht anzeigen

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
