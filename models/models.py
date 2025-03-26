# digital_library/models/models.py
from bson import ObjectId
from datetime import datetime
from typing import List, Optional, Dict, Any

class User:
    def __init__(self, 
                 username: str, 
                 email: str, 
                 password_hash: str, 
                 wallet: float = 0.0):
        """
        User model for digital library
        
        Args:
            username (str): User's username
            email (str): User's email address
            password_hash (str): Hashed password
            wallet (float, optional): User's wallet balance
        """
        self.data = {
            "_id": ObjectId(),
            "username": username,
            "email": email,
            "passwordHash": password_hash,
            "wallet": wallet,
            "createdAt": datetime.utcnow()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return self.data

class Book:
    def __init__(self, 
                 title: str, 
                 author: str, 
                 isbn: str, 
                 published_year: int, 
                 price: float, 
                 categories: Optional[List[str]] = None,
                 description: Optional[str] = None, 
                 imprint: Optional[str] = None):
        """
        Book model representing a book in the digital library
        
        Args:
            title (str): Book title
            author (str): Book author
            isbn (str): International Standard Book Number
            published_year (int): Year of publication
            price (float): Book price
            categories (list, optional): Book categories
            description (str, optional): Book description
            imprint (str, optional): Book publisher
        """
        self.data = {
            "_id": ObjectId(),
            "title": title,
            "author": author,
            "isbn": isbn,
            "publishedYear": published_year,
            "price": price,
            "categories": categories or [],
            "description": description,
            "imprint": imprint,
            "createdAt": datetime.utcnow()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return self.data

class Order:
    def __init__(self, 
                 user_id: ObjectId, 
                 book_ids: List[ObjectId], 
                 total_price: float):
        """
        Order model representing a book purchase
        
        Args:
            user_id (ObjectId): User who made the order
            book_ids (list): List of book IDs in the order
            total_price (float): Total order price
        """
        self.data = {
            "_id": ObjectId(),
            "userId": user_id,
            "orderItems": [{"bookId": book_id} for book_id in book_ids],
            "totalPrice": total_price,
            "orderDate": datetime.utcnow(),
            "status": "pending"  # Add order status
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return self.data

class Review:
    def __init__(self, 
                 user_id: ObjectId, 
                 book_id: ObjectId, 
                 rating: float, 
                 comment: Optional[str] = None):
        """
        Review model representing a book review
        
        Args:
            user_id (ObjectId): User who wrote the review
            book_id (ObjectId): Book being reviewed
            rating (float): Review rating
            comment (str, optional): Review comment
        """
        self.data = {
            "_id": ObjectId(),
            "userId": user_id,
            "bookId": book_id,
            "rating": rating,
            "comment": comment,
            "createdAt": datetime.utcnow()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return self.data

class Category:
    def __init__(self, 
                 name: str, 
                 description: Optional[str] = None):
        """
        Category model for book categorization
        
        Args:
            name (str): Category name
            description (str, optional): Category description
        """
        self.data = {
            "_id": ObjectId(),
            "name": name,
            "description": description,
            "createdAt": datetime.utcnow()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return self.data