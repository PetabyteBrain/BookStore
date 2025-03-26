# views/order_view.py
import tkinter as tk
from models.database import database

class OrderView:
    def __init__(self, root):
        self.root = root  # root ist das Haupt-Tk-Fenster
        self.root.title("Bestellungen")  # Titel des Hauptfensters setzen
        
        self.listbox = tk.Listbox(self.root, width=100, height=20)
        self.listbox.pack(padx=10, pady=10)

        self.load_orders()

    def load_orders(self):
        orders = database.get_all_orders()
        for order in orders:
            order_info = f"Bestell-ID: {order['_id']} - Gesamtpreis: {order['totalPrice']} - Datum: {order['orderDate'].strftime('%Y-%m-%d %H:%M:%S')}"
            self.listbox.insert(tk.END, order_info)
