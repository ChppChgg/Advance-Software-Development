# Import Libraries
import tkinter as tk
from tkinter import ttk, messagebox
import os
import zipfile
import io
import csv

# Import page classes
from HomePage import HomePage
from LoginPage import LoginPage
from SignupPage import SignupPage
from BookingPage import BookingPage

class HorizonMoviesApp:
    def __init__(self, root):
        # Set up main window, title, size, and background color
        self.root = root
        self.root.title("Horizon Movies")
        self.root.geometry("1100x700")
        self.root.configure(bg="#ffffff")
        # Set up a variable to store the current user (if logged in)
        self.current_user = None
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)
        
        # Create a dictionary to store all frames
        # Loop through pages, puts them in same position and stores them in dictionary
        # This allows us to switch between pages easily displaying the page we want on the top
        self.frames = {}
        for F in (LoginPage, SignupPage, HomePage, BookingPage):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure the container to expand
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Start with login page
        # Then loads movies from CSV File, uses 'def load_movies' function line 78 
        self.show_frame("LoginPage")
        self.movies = self.load_movies()
        self.selected_movie = None
    

    def show_frame(self, page_name):
        # Check if user is trying to access restricted pages without being logged in
        # Allow LoginPage and SignupPage without authentication
        if page_name not in ["LoginPage", "SignupPage"] and not self.current_user:
            messagebox.showerror("Access Denied", "Please log in to access this page.")
            self.show_frame("LoginPage")
            return  
        
        # Raises required page to the top
        frame = self.frames[page_name]
        frame.tkraise()
        
        # Update the sidebar for all frames to reflect login status
        for frame_obj in self.frames.values():
            if hasattr(frame_obj, "update_sidebar"):
                frame_obj.update_sidebar()
        
        # Call on_show method if it exists
        if hasattr(frame, "on_show"):
            frame.on_show()
    
    def login_user(self, username):
        """Set the current user and navigate to home page"""
        self.current_user = username
        self.show_frame("HomePage")
    
    def logout_user(self):
        """Clear current user and navigate to login page"""
        self.current_user = None
        self.selected_movie = None
        self.show_frame("LoginPage")
    
    def load_movies(self):
        """Load movie data from CSV file"""
        csv_path = r"HorizonHotelsT/Data/imdb_top_1000.csv"
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                # Skip the first line if it's a comment
                first_line = file.readline()
                if first_line.startswith('//'):
                    reader = csv.DictReader(file)
                else:
                    file.seek(0)  # Reset to beginning of file
                    reader = csv.DictReader(file)
                
                movies = []
                for i, row in enumerate(reader):
                    # Determine status - first 70% of movies as now showing, rest as coming soon
                    status = "now_showing" if i < 70 else "coming_soon"
                    
                    # Extract primary genre
                    genres = row.get("Genre", "").split(",")[0].strip()
                    
                    # Get certificate/rating
                    rating = row.get("Certificate", "")
                    if not rating:
                        rating = "Not Rated"
                    
                    movies.append({
                        "id": i + 1,
                        "title": row.get("Series_Title", f"Movie {i+1}"),
                        "genre": genres,
                        "rating": rating,
                        "status": status
                    })
                    
                return movies if movies else self.load_sample_movies()
                
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            return self.load_sample_movies()
    
    def load_sample_movies(self):
        """Fallback sample movie data"""
        return [
            {"id": 1, "title": "Movie 1", "genre": "Action", "rating": "PG-13", "status": "now_showing"},
            {"id": 2, "title": "Movie 2", "genre": "Comedy", "rating": "PG", "status": "now_showing"},
            {"id": 3, "title": "Movie 3", "genre": "Drama", "rating": "R", "status": "now_showing"},
            {"id": 4, "title": "Movie 4", "genre": "Horror", "rating": "R", "status": "now_showing"},
            {"id": 5, "title": "Movie 5", "genre": "Action", "rating": "PG-13", "status": "now_showing"},
            {"id": 6, "title": "Movie 6", "genre": "Comedy", "rating": "PG", "status": "coming_soon"},
            {"id": 7, "title": "Movie 7", "genre": "Drama", "rating": "R", "status": "coming_soon"},
            {"id": 8, "title": "Movie 8", "genre": "Horror", "rating": "R", "status": "coming_soon"}
        ]


if __name__ == "__main__":
    root = tk.Tk()
    app = HorizonMoviesApp(root)
    root.mainloop()