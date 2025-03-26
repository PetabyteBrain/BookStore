# digital_library/main.py
import tkinter as tk
from views.main_window import DigitalLibraryApp
from config.database import db_connection

def main():
    """
    Main application entry point
    """
    try:
        # Create root window
        root = tk.Tk()
        root.title("Digital Library")
        root.geometry("1024x768")
        
        # Initialize application
        app = DigitalLibraryApp(root, db_connection)
        
        # Start application main loop
        root.mainloop()
    
    except Exception as e:
        print(f"Application startup error: {e}")
    finally:
        # Ensure database connection is closed
        db_connection.close_connection()

if __name__ == "__main__":
    main()