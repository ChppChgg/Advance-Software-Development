"""
Base page, carries sidebar, header, footer, etc.
"""
import tkinter as tk
from tkinter import ttk
from Utility import COLORS, FONTS  

class BasePage(tk.Frame):
    """Base class for all pages with common layout elements"""
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Main container
        self.main_container = tk.Frame(self, bg=COLORS["MAIN_BG"])  # Use COLORS dictionary
        self.main_container.pack(fill="both", expand=True)
        
        # Header frame
        self.header_frame = tk.Frame(self.main_container, bg=COLORS["HEADER_BG"], height=60)  # Use COLORS dictionary
        self.header_frame.pack(fill="x", side="top")
        
        # Logo/Title
        self.title_label = tk.Label(
            self.header_frame, 
            text="HORIZON CINEMAS", 
            font=FONTS["HEADER"],
            bg=COLORS["HEADER_BG"], 
            fg=COLORS["BUTTON_PRIMARY"]  # Change from "white" or TEXT_LIGHT to BUTTON_PRIMARY
        )
        self.title_label.pack(side="left", padx=20, pady=10)
        
        # User info on the right side of header
        self.user_frame = tk.Frame(self.header_frame, bg=COLORS["HEADER_BG"])
        self.user_frame.pack(side="right", padx=20)
        
        self.username_label = tk.Label(
            self.user_frame, 
            text="Guest", 
            font=("Arial", 12),
            bg=COLORS["HEADER_BG"], 
            fg="white"
        )
        self.username_label.pack(side="left", padx=5)
        
        # Body container with sidebar and content area
        self.body_container = tk.Frame(self.main_container)
        self.body_container.pack(fill="both", expand=True)
        
        # Sidebar frame
        self.sidebar_frame = tk.Frame(self.body_container, bg=COLORS["SIDEBAR_BG"], width=180)  # Use COLORS dictionary
        self.sidebar_frame.pack(fill="y", side="left")
        self.sidebar_frame.pack_propagate(False)  # Prevent the frame from shrinking
        
        # Sidebar title
        self.sidebar_title = tk.Label(
            self.sidebar_frame,
            text="NAVIGATION",
            font=("Arial", 12, "bold"),
            bg=COLORS["SIDEBAR_BG"],  # Use COLORS dictionary
            fg="white"
        )
        self.sidebar_title.pack(pady=(20, 10))
        
        # Frame for navigation buttons (top)
        self.sidebar_nav_frame = tk.Frame(self.sidebar_frame, bg=COLORS["SIDEBAR_BG"])
        self.sidebar_nav_frame.pack(fill="both", expand=True, side="top")

        # Frame for logout button (bottom)
        self.sidebar_logout_frame = tk.Frame(self.sidebar_frame, bg=COLORS["SIDEBAR_BG"])
        self.sidebar_logout_frame.pack(fill="x", side="bottom", pady=10)

        self.nav_buttons = {}
        
        # Content frame - this will be filled by child classes
        self.content_frame = tk.Frame(self.body_container, bg=COLORS["CONTENT_BG"])  # Use COLORS dictionary
        self.content_frame.pack(fill="both", expand=True, side="right")
        
        # Footer
        self.footer_frame = tk.Frame(self.main_container, bg=COLORS["HEADER_BG"], height=30)  # Use COLORS dictionary
        self.footer_frame.pack(fill="x", side="bottom")
        
        self.footer_label = tk.Label(
            self.footer_frame,
            text="© 2024 Horizon Cinemas",
            font=("Arial", 9),
            bg=COLORS["HEADER_BG"],  # Use COLORS dictionary
            fg="white"
        )
        self.footer_label.pack(pady=5)
        
    def update_sidebar(self, is_logged_in=False, is_admin=False):
        """Update sidebar based on login status and user role"""
        # Clear existing buttons
        for widget in self.sidebar_nav_frame.winfo_children():
            widget.destroy()
        for widget in self.sidebar_logout_frame.winfo_children():
            widget.destroy()
        
        self.nav_buttons = {}
        
        # Basic navigation for all users
        self.add_nav_button("Home", lambda: self.controller.show_frame("HomePage"), parent=self.sidebar_nav_frame)
        
        if not is_logged_in:
            self.add_nav_button("Login", lambda: self.controller.show_frame("LoginPage"), parent=self.sidebar_nav_frame)
            self.add_nav_button("Sign Up", lambda: self.controller.show_frame("SignupPage"), parent=self.sidebar_nav_frame)
        else:
            self.add_nav_button("Book Tickets", lambda: self.controller.show_frame("BookingPage"), parent=self.sidebar_nav_frame)
            self.add_nav_button("My Bookings", lambda: self.controller.show_frame("CancellationPage"), parent=self.sidebar_nav_frame)
            
            # Admin-specific navigation
            if is_admin:
                self.add_nav_button("Admin Panel", lambda: self.controller.show_frame("AdminPage"), parent=self.sidebar_nav_frame)
                self.add_nav_button("Manager View", lambda: self.controller.show_frame("ManagerPage"), parent=self.sidebar_nav_frame)
            
            # Logout button at the bottom
            self.add_nav_button("Logout", self.controller.logout, parent=self.sidebar_logout_frame)
            
    def add_nav_button(self, text, command, parent=None):
        """Add a navigation button to the sidebar"""
        if parent is None:
            parent = self.sidebar_frame
        button = tk.Button(
            parent,
            text=text,
            font=("Arial", 11),
            bg=COLORS["SIDEBAR_BG"],  # Use COLORS dictionary
            fg="white",
            bd=0,
            pady=8,
            padx=15,
            highlightthickness=0,
            activebackground=COLORS["BUTTON_ACTIVE"],  # Use COLORS dictionary
            activeforeground="white",
            anchor="w",
            width=15,
            command=command
        )
        button.pack(fill="x", padx=5, pady=2)
        self.nav_buttons[text] = button
        
    def update_user_info(self, username=None):
        """Update the username display in the header"""
        if username:
            self.current_username = username
            self.username_label.config(text=f"Welcome, {username}")
        else:
            self.current_username = None
            self.username_label.config(text="Guest")
            