from pymongo import MongoClient
from config.settings import MONGO_URI, DATABASE_NAME

class Database:
    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[DATABASE_NAME]
            self.books_collection = self.db["books"]
            self.users_collection = self.db["users"]
            self.orders_collection = self.db["orders"]
            print("✅ Erfolgreich mit der Datenbank verbunden")
        except Exception as e:
            print(f"❌ Fehler bei der Datenbankverbindung: {e}")

    def insert_book(self, book_data):
        """Fügt ein neues Buch in die Datenbank ein."""
        return self.books_collection.insert_one(book_data)

    def get_all_books(self):
        """Ruft alle Bücher aus der Datenbank ab."""
        return list(self.books_collection.find({}, {"_id": 0}))

    def insert_order(self, order_data):
        """Speichert eine Bestellung in der Datenbank."""
        return self.orders_collection.insert_one(order_data)

    def get_orders_by_user(self, user_id):
        """Holt alle Bestellungen eines Nutzers."""
        return list(self.orders_collection.find({"user_id": user_id}, {"_id": 0}))
    
    def get_all_orders(self):
        # Bestellungen aus der Datenbank abrufen und zurückgeben
        return list(self.orders_collection.find({}))

database = Database()
