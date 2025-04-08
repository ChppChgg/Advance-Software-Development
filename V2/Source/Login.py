"""
Login page 
"""
import tkinter as tk
from tkinter import ttk, messagebox
from Basepage import BasePage
from Utility import COLORS, FONTS
from Database import Database

class LoginPage(BasePage):
    """Login page for user authentication"""
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        
        # Initialize database connection
        self.db = Database()
        
        # Content area
        content = tk.Frame(self.content_frame, bg=COLORS["CONTENT_BG"])
        content.pack(fill="both", expand=True)
        
        # Login form container - centered
        form_frame = tk.Frame(content, bg=COLORS["CONTENT_BG"])
        form_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title_label = tk.Label(
            form_frame,
            text="Login to Your Account",
            font=FONTS["TITLE"],
            bg=COLORS["CONTENT_BG"]
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Username field
        username_label = tk.Label(
            form_frame,
            text="Username:",
            font=FONTS["NORMAL"],
            bg=COLORS["CONTENT_BG"]
        )
        username_label.grid(row=1, column=0, sticky="w", pady=10)
        
        self.username_entry = tk.Entry(form_frame, font=FONTS["NORMAL"], width=25)
        self.username_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Password field
        password_label = tk.Label(
            form_frame,
            text="Password:",
            font=FONTS["NORMAL"],
            bg=COLORS["CONTENT_BG"]
        )
        password_label.grid(row=2, column=0, sticky="w", pady=10)
        
        self.password_entry = tk.Entry(form_frame, font=FONTS["NORMAL"], width=25, show="*")
        self.password_entry.grid(row=2, column=1, pady=10, padx=10)
        
        # Login button
        login_button = tk.Button(
            form_frame,
            text="Login",
            font=FONTS["BUTTON"],
            bg=COLORS["BUTTON_PRIMARY"],
            fg=COLORS["TEXT_LIGHT"],
            padx=20,
            pady=8,
            command=self.login_user
        )
        login_button.grid(row=3, column=0, columnspan=2, pady=30)
        
        # Sign up link
        signup_link = tk.Label(
            form_frame,
            text="Don't have an account? Sign up",
            font=FONTS["SMALL"],
            fg="blue",
            bg=COLORS["CONTENT_BG"],
            cursor="hand2"
        )
        signup_link.grid(row=4, column=0, columnspan=2)
        signup_link.bind("<Button-1>", lambda e: controller.show_frame("SignupPage"))
        
        # Error message label
        self.error_label = tk.Label(
            form_frame,
            text="",
            font=FONTS["SMALL"],
            fg="red",
            bg=COLORS["CONTENT_BG"]
        )
        self.error_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        # Bind Enter key to login function
        self.username_entry.bind("<Return>", lambda event: self.login_user())
        self.password_entry.bind("<Return>", lambda event: self.login_user())
        
    def login_user(self):
        """Handle user login verification and process"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Basic validation
        if not username or not password:
            self.error_label.config(text="Username and password are required")
            return
            
        # Verify credentials using database
        user = self.db.authenticate_user(username, password)
        
        if user:
            # Clear any error messages
            self.error_label.config(text="")
            
            # Reset form
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            
            # Check if admin or manager
            is_admin = user['RoleName'] in ['Admin', 'Manager']
            
            # Login the user through the controller
            self.controller.login(user['Username'], is_admin)
            
            messagebox.showinfo("Login Successful", f"Welcome back, {user['Username']}!")
        else:
            self.error_label.config(text="Invalid username or password")