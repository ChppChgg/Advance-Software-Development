"""
Utility functions for the application
"""
import re
import hashlib
import random
import string
from datetime import datetime, timedelta

#Harry Elson, 23021935
#Matt Nogodula, 23015215
#Jerry Lin, 23024553

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

