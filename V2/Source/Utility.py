"""
Utility functions for the application
"""
import re
import hashlib
import random
import string
from datetime import datetime, timedelta

# Color scheme constants for consistent application styling
COLORS = {
    "MAIN_BG": "#F9F9F9",        # Light gray background behind main content
    "HEADER_BG": "#000000",      # Black header (as seen in the screenshot)
    "SIDEBAR_BG": "#23272A",     # Dark gray/charcoal sidebar or dropdown
    "CONTENT_BG": "#FFFFFF",     # White content area
    "BUTTON_ACTIVE": "#FF7F50",  # Lighter orange (hover/active state)
    "BUTTON_PRIMARY": "#FF6600", # Primary button color (vivid orange)
    "BUTTON_CANCEL": "#DF4759",  # Red for cancel/delete actions (unchanged)
    "TEXT_LIGHT": "#FFFFFF",     # White text for dark backgrounds
    "TEXT_DARK": "#333333"       # Dark text for light backgrounds
}

# Font constants
FONTS = {
    "HEADER": ("Arial", 18, "bold"),
    "TITLE": ("Arial", 16, "bold"),
    "SUBTITLE": ("Arial", 14, "bold"),
    "NORMAL": ("Arial", 12),
    "SMALL": ("Arial", 10),
    "BUTTON": ("Arial", 12, "bold"),
    "FOOTER": ("Arial", 9)
}

def validate_email(email):
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def validate_password(password):
    """
    Validate password strength
    Requires minimum 8 characters, at least one letter and one number
    """
    if len(password) < 8:
        return False
    if not any(c.isalpha() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_booking_reference():
    """Generate a random booking reference"""
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=4))
    return f"{letters}-{numbers}"

def get_future_dates(days=14):
    """Get a list of future dates for the next n days"""
    dates = []
    today = datetime.now()
    for i in range(days):
        date = today + timedelta(days=i)
        dates.append(date.strftime("%Y-%m-%d"))
    return dates

def format_currency(amount):
    """Format amount as currency"""
    return f"£{amount:.2f}"

def calculate_cancellation_fee(booking_date, cancellation_date):
    """
    Calculate cancellation fee based on how close to the screening date
    Returns a percentage (0-100)
    """
    # Convert strings to datetime objects if needed
    if isinstance(booking_date, str):
        booking_date = datetime.strptime(booking_date, "%Y-%m-%d %H:%M:%S")
    if isinstance(cancellation_date, str):
        cancellation_date = datetime.now()
    
    # Calculate time difference in hours
    time_diff = (booking_date - cancellation_date).total_seconds() / 3600
    
    # Within 24 hours: 100% fee (no refund)
    if time_diff <= 24:
        return 100
    # 24-48 hours: 50% fee
    elif time_diff <= 48:
        return 50
    # 48-72 hours: 25% fee
    elif time_diff <= 72:
        return 25
    # More than 72 hours: 10% fee
    else:
        return 10