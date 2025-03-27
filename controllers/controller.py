# digital_library/controllers/controller.py
import tkinter as tk
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
    
    # Existing methods remain the same, but add helper method for ObjectId conversion
    def _convert_objectid_to_str(self, data):
        """
        Recursively convert ObjectId to string in nested dictionaries
        
        Args:
            data (dict or list): Data to convert
        
        Returns:
            Converted data with ObjectId converted to strings
        """
        if isinstance(data, dict):
            return {
                k: (str(v) if isinstance(v, ObjectId) else 
                    self._convert_objectid_to_str(v)) 
                for k, v in data.items()
            }
        elif isinstance(data, list):
            return [self._convert_objectid_to_str(item) for item in data]
        return data
    
    def search_books(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search books based on various criteria
        
        Args:
            query (dict): Search criteria
        
        Returns:
            List of matching books with ObjectIds converted to strings
        """
        books = list(self.db.books.find(query))
        return [self._convert_objectid_to_str(book) for book in books]
    
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
            # Ensure user_id and book_ids are ObjectId
            user_obj_id = ObjectId(user_id)
            book_obj_ids = [ObjectId(bid) for bid in book_ids]
            
            # Fetch book prices
            books = list(self.db.books.find({"_id": {"$in": book_obj_ids}}))
            total_price = sum(book['price'] for book in books)
            
            # Create order
            new_order = {
                'user_id': user_obj_id,
                'book_ids': book_obj_ids,
                'total_price': total_price,
                'order_date': tk.datetime.now()  # You might want to import datetime
            }
            
            result = self.db.orders.insert_one(new_order)
            
            return {
                "success": True, 
                "message": "Order created successfully",
                "order_id": str(result.inserted_id),
                "total_price": total_price
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    def add_book(self, book_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new book to the database

        Args:
            book_data (dict): Dictionary containing book information

        Returns:
            Dict containing book addition result
        """
        try:
            # Validate required fields
            required_fields = ['title', 'author', 'isbn', 'published_year', 'price']
            for field in required_fields:
                if not book_data.get(field):
                    return {
                        "success": False, 
                        "message": f"Missing required field: {field}"
                    }

            # Prepare book data for insertion
            new_book = {
                'title': book_data['title'],
                'author': book_data['author'],
                'isbn': book_data['isbn'],
                'publishedYear': book_data['published_year'],
                'price': book_data['price'],
                'categories': book_data.get('categories', []),
                'description': book_data.get('description', ''),
                'imprint': book_data.get('imprint', '')
            }

            # Insert the book
            result = self.db.books.insert_one(new_book)

            return {
                "success": True, 
                "message": "Book added successfully",
                "book_id": str(result.inserted_id)
            }

        except Exception as e:
            return {
                "success": False, 
                "message": f"Error adding book: {str(e)}"
            }
    
    def edit_book(self, original_isbn: str, book_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Edit a book in the database
        
        Args:
            original_isbn (str): Original ISBN to identify the book
            book_data (dict): Updated book information
        
        Returns:
            Dict containing book edit result
        """
        try:
            # Validate required fields
            required_fields = ['title', 'author', 'isbn', 'published_year', 'price']
            for field in required_fields:
                if not book_data.get(field):
                    return {
                        "success": False, 
                        "message": f"Missing required field: {field}"
                    }
            
            # Prepare book data for update
            update_data = {
                'title': book_data['title'],
                'author': book_data['author'],
                'isbn': book_data['isbn'],
                'publishedYear': book_data['published_year'],
                'price': book_data['price'],
                'categories': book_data.get('categories', []),
                'description': book_data.get('description', ''),
                'imprint': book_data.get('imprint', '')
            }
            
            # Try multiple ways to find the book
            result = self.db.books.update_one(
                # Try multiple query methods to find the book
                {
                    '$or': [
                        {'isbn': original_isbn},  # Exact ISBN match
                        {'isbn': {'$regex': f'^{original_isbn}$', '$options': 'i'}},  # Case-insensitive exact match
                        {'isbn': str(original_isbn)}  # Ensure string conversion
                    ]
                },
                {'$set': update_data}
            )
            
            if result.modified_count > 0:
                return {
                    "success": True, 
                    "message": "Book updated successfully"
                }
            else:
                # If no book was found, provide more diagnostic information
                # Try to find why the book wasn't found
                existing_book = self.db.books.find_one({'isbn': original_isbn})
                
                if existing_book:
                    print(f"Existing book found: {existing_book}")
                    return {
                        "success": False, 
                        "message": "Book found but not updated. Check data types and field names."
                    }
                else:
                    return {
                        "success": False, 
                        "message": f"No book found with ISBN: {original_isbn}"
                    }
        
        except Exception as e:
            return {
                "success": False, 
                "message": f"Error updating book: {str(e)}"
            }
        
    def delete_book(self, isbn):
        """
        Delete a book from the database by ISBN

        Args:
            isbn: ISBN of the book to delete (can be int or str)

        Returns:
            Dict containing book deletion result
        """
        try:
            # Convert isbn to string if it's not already a string
            isbn = str(isbn).strip()

            # First, try to find the book to understand why it's not being found
            existing_book = self.db.books.find_one({'isbn': isbn})

            if existing_book:
                # Print out the book details for debugging
                print("Book found:", existing_book)

                # Ensure case-insensitive and whitespace-stripped comparison
                result = self.db.books.delete_one({
                    'isbn': {'$regex': f'^{isbn}$', '$options': 'i'}
                })

                if result.deleted_count > 0:
                    return {
                        "success": True, 
                        "message": "Book deleted successfully"
                    }
                else:
                    return {
                        "success": False, 
                        "message": "Book found but could not be deleted"
                    }
            else:
                # Try more flexible search methods
                # Look for partial matches or whitespace variations
                flexible_search = self.db.books.find_one({
                    'isbn': {'$regex': f'{isbn}', '$options': 'i'}
                })

                if flexible_search:
                    print("Flexible match found:", flexible_search)
                    result = self.db.books.delete_one({'_id': flexible_search['_id']})

                    if result.deleted_count > 0:
                        return {
                            "success": True, 
                            "message": "Book deleted successfully (flexible match)"
                        }

                return {
                    "success": False, 
                    "message": f"No book found with ISBN: {isbn}"
                }

        except Exception as e:
            return {
                "success": False, 
                "message": f"Error deleting book: {str(e)}"
            }