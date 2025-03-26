# digital_library/controllers/controller.py
from typing import List, Dict, Any
from bson import ObjectId
from config.database import db_connection
from models.models import Book, User, Order, Review
from utils.helpers import validate_email, hash_password, validate_password_strength

class LibraryController:
    def __init__(self, db_connection):
        """
        Main controller for digital library operations
        
        Args:
            db_connection (DatabaseConnection): Database connection
        """
        self.db = db_connection
    
    # User Management
    def register_user(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """
        Register a new user
        
        Args:
            username (str): Username
            email (str): Email address
            password (str): Password
        
        Returns:
            Dict containing registration result
        """
        # Validate input
        if not validate_email(email):
            return {"success": False, "message": "Invalid email format"}
        
        if not validate_password_strength(password):
            return {"success": False, "message": "Password does not meet complexity requirements"}
        
        # Check if user already exists
        existing_user = self.db.users.find_one({"$or": [
            {"username": username},
            {"email": email}
        ]})
        
        if existing_user:
            return {"success": False, "message": "Username or email already exists"}
        
        # Create user
        hashed_password = hash_password(password)
        new_user = User(username, email, hashed_password)
        result = self.db.users.insert_one(new_user.to_dict())
        
        return {
            "success": True, 
            "message": "User registered successfully",
            "user_id": str(result.inserted_id)
        }
    
    # Book Management
    def add_book(self, book_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new book to the library
        
        Args:
            book_data (dict): Book details
        
        Returns:
            Dict containing book addition result
        """
        try:
            new_book = Book(
                title=book_data['title'],
                author=book_data['author'],
                isbn=book_data['isbn'],
                published_year=book_data['published_year'],
                price=book_data['price'],
                categories=book_data.get('categories', []),
                description=book_data.get('description'),
                imprint=book_data.get('imprint')
            )
            result = self.db.books.insert_one(new_book.to_dict())
            
            return {
                "success": True, 
                "message": "Book added successfully",
                "book_id": str(result.inserted_id)
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def search_books(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search books based on various criteria
        
        Args:
            query (dict): Search criteria
        
        Returns:
            List of matching books
        """
        return list(self.db.books.find(query))
    
    # Order Management
    def create_order(self, user_id: str, book_ids: List[str]) -> Dict[str, Any]:
        """
        Create a new order
        
        Args:
            user_id (str): User placing the order
            book_ids (list): Books to be ordered
        
        Returns:
            Dict containing order creation result
        """
        try:
            # Fetch book prices
            books = list(self.db.books.find({"_id": {"$in": [ObjectId(bid) for bid in book_ids]}}))
            total_price = sum(book['price'] for book in books)
            
            # Create order
            new_order = Order(
                user_id=ObjectId(user_id), 
                book_ids=[ObjectId(bid) for bid in book_ids], 
                total_price=total_price
            )
            
            result = self.db.orders.insert_one(new_order.to_dict())
            
            return {
                "success": True, 
                "message": "Order created successfully",
                "order_id": str(result.inserted_id),
                "total_price": total_price
            }
        except Exception as e:
            return {"success": False, "message": str(e)}