""" 
Signup page implementation
"""
import tkinter as tk
from tkinter import ttk, messagebox
from Basepage import BasePage
from Utility import COLORS, FONTS, validate_email, validate_password
from Database import Database

class SignupPage(BasePage):
    """Signup page for user registration"""
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        
        # Initialize database connection
        self.db = Database()
        
        # Content area
        content = tk.Frame(self.content_frame, bg=COLORS["CONTENT_BG"])
        content.pack(fill="both", expand=True)
        
        # Signup form container - centered
        form_frame = tk.Frame(content, bg=COLORS["CONTENT_BG"])
        form_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title_label = tk.Label(
            form_frame,
            text="Create an Account",
            font=FONTS["TITLE"],
            bg=COLORS["CONTENT_BG"]
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Full Name field
        name_label = tk.Label(
            form_frame,
            text="Full Name:",
            font=FONTS["NORMAL"],
            bg=COLORS["CONTENT_BG"]
        )
        name_label.grid(row=1, column=0, sticky="w", pady=10)
        
        self.name_entry = tk.Entry(form_frame, font=FONTS["NORMAL"], width=25)
        self.name_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Email field
        email_label = tk.Label(
            form_frame,
            text="Email:",
            font=FONTS["NORMAL"],
            bg=COLORS["CONTENT_BG"]
        )
        email_label.grid(row=2, column=0, sticky="w", pady=10)
        
        self.email_entry = tk.Entry(form_frame, font=FONTS["NORMAL"], width=25)
        self.email_entry.grid(row=2, column=1, pady=10, padx=10)
        
        # Username field
        username_label = tk.Label(
            form_frame,
            text="Username:",
            font=FONTS["NORMAL"],
            bg=COLORS["CONTENT_BG"]
        )
        username_label.grid(row=3, column=0, sticky="w", pady=10)
        
        self.username_entry = tk.Entry(form_frame, font=FONTS["NORMAL"], width=25)
        self.username_entry.grid(row=3, column=1, pady=10, padx=10)
        
        # Password field
        password_label = tk.Label(
            form_frame,
            text="Password:",
            font=FONTS["NORMAL"],
            bg=COLORS["CONTENT_BG"]
        )
        password_label.grid(row=4, column=0, sticky="w", pady=10)
        
        self.password_entry = tk.Entry(form_frame, font=FONTS["NORMAL"], width=25, show="*")
        self.password_entry.grid(row=4, column=1, pady=10, padx=10)
        
        # Confirm Password field
        confirm_label = tk.Label(
            form_frame,
            text="Confirm Password:",
            font=FONTS["NORMAL"],
            bg=COLORS["CONTENT_BG"]
        )
        confirm_label.grid(row=5, column=0, sticky="w", pady=10)
        
        self.confirm_entry = tk.Entry(form_frame, font=FONTS["NORMAL"], width=25, show="*")
        self.confirm_entry.grid(row=5, column=1, pady=10, padx=10)
        
        # Signup button
        signup_button = tk.Button(
            form_frame,
            text="Sign Up",
            font=FONTS["BUTTON"],
            bg=COLORS["BUTTON_PRIMARY"],
            fg=COLORS["TEXT_LIGHT"],
            padx=20,
            pady=8,
            command=self.signup_user
        )
        signup_button.grid(row=6, column=0, columnspan=2, pady=30)
        
        # Login link
        login_link = tk.Label(
            form_frame,
            text="Already have an account? Login",
            font=FONTS["SMALL"],
            fg="blue",
            bg=COLORS["CONTENT_BG"],
            cursor="hand2"
        )
        login_link.grid(row=7, column=0, columnspan=2)
        login_link.bind("<Button-1>", lambda e: controller.show_frame("LoginPage"))
        
        # Error message label
        self.error_label = tk.Label(
            form_frame,
            text="",
            font=FONTS["SMALL"],
            fg="red",
            bg=COLORS["CONTENT_BG"]
        )
        self.error_label.grid(row=8, column=0, columnspan=2, pady=(10, 0))
    
    def signup_user(self):
        """Handle user registration process"""
        # Get form values
        full_name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_entry.get()
        
        # Reset error message
        self.error_label.config(text="")
        
        # Validate input fields
        if not full_name:
            self.error_label.config(text="Please enter your full name")
            return
            
        if not email:
            self.error_label.config(text="Please enter your email address")
            return
            
        if not validate_email(email):
            self.error_label.config(text="Please enter a valid email address")
            return
            
        if not username:
            self.error_label.config(text="Please enter a username")
            return
            
        if len(username) < 4:
            self.error_label.config(text="Username must be at least 4 characters")
            return
            
        if not password:
            self.error_label.config(text="Please enter a password")
            return
            
        if not validate_password(password):
            self.error_label.config(text="Password must be at least 8 characters with letters and numbers")
            return
            
        if password != confirm_password:
            self.error_label.config(text="Passwords do not match")
            return
        
        # Try to create the user
        success, message = self.db.create_user(username, password, email, "Customer")
        
        if success:
            # Reset form
            self.name_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.confirm_entry.delete(0, 'end')
            
            # Show success message
            messagebox.showinfo("Registration Successful", 
                               "Your account has been created successfully. You can now login.")
            
            # Create customer record
            self.db.add_customer(full_name, email, "")
            
            # Switch to login page
            self.controller.show_frame("LoginPage")
        else:
            # Show error message
            self.error_label.config(text=message)