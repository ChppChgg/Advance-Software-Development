""" 
Main file to open application
"""
import tkinter as tk
from tkinter import ttk  # Add ttk import for styling
import os
from Basepage import BasePage
from Home import HomePage
from Login import LoginPage
from Signup import SignupPage
from Booking import BookingPage
from Cancel import CancellationPage
from Admin import AdminPage
from Manager import ManagerPage
from Utility import COLORS  # Import colors from utility
from Database import Database

class HorizonCinemas(tk.Tk):
    """Main application class"""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Setup the window
        self.title("Horizon Cinemas")
        self.geometry("1000x700")
        self.minsize(900, 600)
        
        # Application state
        self.user = None
        self.is_admin = False
        
        # Configure app-wide styles
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        style.configure("TCombobox", font=("Arial", 12))
        
        # Setup the container frame for all pages
        container = tk.Frame(self, bg=COLORS["MAIN_BG"])
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Initialize pages dictionary
        self.frames = {}
        
        # Create all page instances
        for F in (HomePage, LoginPage, SignupPage, 
                  BookingPage, CancellationPage, 
                  AdminPage, ManagerPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            
            # Put all pages in the same location
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show the home page by default
        self.show_frame("HomePage")
    
    def show_frame(self, page_name):
        """Show the specified page and update sidebar"""
        frame = self.frames[page_name]
        frame.tkraise()
        
        # Update sidebar for all pages
        for frame_name, frame_instance in self.frames.items():
            frame_instance.update_sidebar(
                is_logged_in=self.user is not None,
                is_admin=self.is_admin
            )
            frame_instance.update_user_info(self.user)
    
    def login(self, username, is_admin=False):
        """Handle user login"""
        self.user = username
        self.is_admin = is_admin
        self.show_frame("HomePage")
    
    def logout(self):
        """Handle user logout"""
        self.user = None
        self.is_admin = False
        self.show_frame("HomePage")

def run_application():
    """Function to run the Horizon Cinemas application"""
    db = Database()
    db.insert_initial_films()
    app = HorizonCinemas()
    app.mainloop()

if __name__ == "__main__":
    run_application()