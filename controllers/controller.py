from models.database import database
from views.book_view import BookView
from views.order_view import OrderView

class Controller:
    def __init__(self, root):
        self.root = root
        self.current_view = None

    def show_book_view(self):
        """Zeigt die Buchansicht."""
        self.clear_view()
        self.current_view = BookView(self.root)
        self.current_view.pack(fill="both", expand=True)

    def show_order_view(self):
        # Bestellansicht anzeigen
        self.current_view = OrderView(self.root)  # root sollte Tk sein, kein Frame

    def clear_view(self):
        """Löscht die aktuelle Ansicht, bevor eine neue geladen wird."""
        if self.current_view:
            self.current_view.destroy()
