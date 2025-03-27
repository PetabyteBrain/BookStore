# digital_library/config/database.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnection:
    def __init__(self, 
                 host='localhost', 
                 port=27017, 
                 database='db'):  # Changed default database name to 'db'
        """
        Initialize MongoDB connection
        
        Args:
            host (str): MongoDB host
            port (int): MongoDB port
            database (str): Database name
        """
        try:
            # Create connection
            self.client = MongoClient(host, port)
            self.db = self.client[database]
            
            # Collections
            self.books = self.db['books']
            self.users = self.db['users']
            self.orders = self.db['orders']
            self.reviews = self.db['reviews']
            self.categories = self.db['categories']
            
            print("Successfully connected to MongoDB")
        
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
    
    def close_connection(self):
        """Close the MongoDB connection"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

# Global database connection
db_connection = DatabaseConnection()