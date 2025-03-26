# digital_library/utils/helpers.py
import re
import hashlib
import secrets

def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email (str): Email address to validate
    
    Returns:
        bool: True if email is valid, False otherwise
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def hash_password(password: str) -> str:
    """
    Hash password using SHA-256
    
    Args:
        password (str): Plain text password
    
    Returns:
        str: Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()

def generate_salt() -> str:
    """
    Generate a cryptographically secure random salt
    
    Returns:
        str: Random salt
    """
    return secrets.token_hex(16)

def validate_password_strength(password: str) -> bool:
    """
    Check password strength
    
    Args:
        password (str): Password to check
    
    Returns:
        bool: True if password meets complexity requirements
    """
    # At least 8 characters, one uppercase, one lowercase, one number
    return (len(password) >= 8 and 
            any(c.isupper() for c in password) and 
            any(c.islower() for c in password) and 
            any(c.isdigit() for c in password))

def format_currency(amount: float) -> str:
    """
    Format amount as currency
    
    Args:
        amount (float): Amount to format
    
    Returns:
        str: Formatted currency string
    """
    return f"€{amount:.2f}"