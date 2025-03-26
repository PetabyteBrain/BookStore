from bson import ObjectId

class Book:
    def __init__(self, title, year, genre, author, _id=None):
        """Repräsentiert ein Buch-Objekt."""
        self._id = _id or ObjectId()
        self.title = title
        self.year = year
        self.genre = genre
        self.author = author

    def to_dict(self):
        """Konvertiert das Buch in ein Dictionary-Format für MongoDB."""
        return {
            "_id": self._id,
            "title": self.title,
            "year": self.year,
            "genre": self.genre,
            "author": self.author
        }

    @classmethod
    def from_dict(cls, data):
        """Erstellt ein Buch-Objekt aus einem Dictionary."""
        return cls(data["title"], data["year"], data["genre"], data["author"], data["_id"])

class User:
    def __init__(self, username, email, _id=None):
        """Repräsentiert einen Nutzer."""
        self._id = _id or ObjectId()
        self.username = username
        self.email = email

    def to_dict(self):
        """Konvertiert den Nutzer in ein Dictionary-Format für MongoDB."""
        return {
            "_id": self._id,
            "username": self.username,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data):
        """Erstellt ein Nutzer-Objekt aus einem Dictionary."""
        return cls(data["username"], data["email"], data["_id"])

class Order:
    def __init__(self, user_id, book_id, _id=None):
        """Repräsentiert eine Bestellung eines Nutzers für ein Buch."""
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.book_id = book_id

    def to_dict(self):
        """Konvertiert die Bestellung in ein Dictionary-Format für MongoDB."""
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "book_id": self.book_id
        }

    @classmethod
    def from_dict(cls, data):
        """Erstellt eine Bestellung aus einem Dictionary."""
        return cls(data["user_id"], data["book_id"], data["_id"])
