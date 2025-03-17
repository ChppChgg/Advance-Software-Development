import tkinter as tk
from BasePage import BasePage

class HomePage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        self.welcome_label = tk.Label(self.content, text="Welcome, Guest", 
                                    font=("Helvetica", 18), bg="white")
        self.welcome_label.pack(anchor="w", padx=20, pady=20)
        self.create_movie_section("Now Showing", "now_showing")
        self.create_movie_section("Coming Soon", "coming_soon")
    
    def create_movie_section(self, title, status):
        """Create a section of movies with the given status"""
        section_frame = tk.Frame(self.content, bg="white")
        section_frame.pack(fill="x", padx=20, pady=10)
        section_title = tk.Label(section_frame, text=title, font=("Helvetica", 16, "bold"), 
                               bg="white", fg="#ff4500")
        section_title.pack(anchor="w", pady=(10, 15))
        movie_container = tk.Frame(section_frame, bg="white")
        movie_container.pack(fill="x")
        
    def on_show(self):
        """Update welcome message and movies when page is shown"""
        if not self.controller.current_user:
            # If no user is logged in, redirect to login page
            self.controller.show_frame("LoginPage")
            return
    
        username = self.controller.current_user
        self.welcome_label.config(text=f"Welcome, {username}")
        self.populate_movies()
    
    def populate_movies(self):
        """Populate movie grids with movie data"""
        # Clear existing content
        for widget in self.content.winfo_children()[1:]:  
            for child in widget.winfo_children()[1:]: 
                child.destroy()
        now_showing_container = tk.Frame(self.content.winfo_children()[1], bg="white")  # first section
        now_showing_container.pack(fill="x")
        coming_soon_container = tk.Frame(self.content.winfo_children()[2], bg="white")  # second section
        coming_soon_container.pack(fill="x")
        now_showing = [m for m in self.controller.movies if m["status"] == "now_showing"]
        coming_soon = [m for m in self.controller.movies if m["status"] == "coming_soon"]
        now_showing = now_showing[:8]
        coming_soon = coming_soon[:8]
        self.create_movie_frames(now_showing_container, now_showing, True)
        self.create_movie_frames(coming_soon_container, coming_soon, False)
    
    def create_movie_frames(self, container, movies, bookable):
        """Create visual frames for each movie"""
        movie_grid = tk.Frame(container, bg="white")
        movie_grid.pack(fill="x")
        
        # Add each movie
        for i, movie in enumerate(movies):
            # Create fixed size frame for consistent display
            movie_frame = tk.Frame(movie_grid, bg="white", bd=1, relief="solid",
                                  width=180, height=270)
            movie_frame.grid(row=i//4, column=i%4, padx=10, pady=10)
            movie_frame.grid_propagate(False)  # Fixed size
            
            # Movie title with fixed height
            title_frame = tk.Frame(movie_frame, bg="white", height=60, width=160)
            title_frame.pack(pady=(15, 5))
            title_frame.pack_propagate(False)
            
            title_label = tk.Label(title_frame, text=movie["title"], bg="white", 
                                  font=("Helvetica", 12, "bold"), wraplength=160)
            title_label.pack()
            
            # Movie details
            details = f"Genre: {movie['genre']}\nRating: {movie['rating']}"
            details_label = tk.Label(movie_frame, text=details, bg="white")
            details_label.pack(pady=10)
            
            # Button - "Book Now" or "Coming Soon"
            button_text = "Book Now" if bookable else "Coming Soon"
            button_color = "#ff4500" if bookable else "#3498db"
            button_command = lambda m=movie: self.book_movie(m) if bookable else None
            
            book_button = tk.Button(movie_frame, text=button_text, bg=button_color, fg="white",
                                  command=button_command)
            book_button.pack(side="bottom", pady=15)
    
    def book_movie(self, movie):
        """Start booking process for a movie"""
        self.controller.selected_movie = movie
        self.controller.show_frame("BookingPage")
