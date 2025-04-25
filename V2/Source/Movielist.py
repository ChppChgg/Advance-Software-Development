import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Basepage import BasePage
from Database import Database
import os


class MovieListPage(BasePage):
    """Page that lists all movies with details"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        
        # Initialize to hold image references
        self.image_references = []
        
        # Main container frame
        main_frame = tk.Frame(self.content_frame, bg="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        page_title = tk.Label(main_frame, text="All Movies", font=("Arial", 16, "bold"), bg="white")
        page_title.pack(anchor="w", pady=(0, 20))

        # Create scrollable canvas
        canvas = tk.Canvas(main_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        # Configure canvas scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.db = Database()
        movies = self.db.get_all_film_rows()  # Pull all films

        for movie in movies:
            frame = tk.Frame(scrollable_frame, bg="white", bd=1, relief="solid")
            frame.pack(fill="x", padx=5, pady=10)

            # Generate expected image filename
            expected_image = f"{movie['Title'].lower().replace(' ', '')}.jfif"
            poster_path = f"V2/Source/images/{expected_image}"

            try:
                # Try to load the image
                img = Image.open(poster_path)
                img = img.resize((120, 180))
                photo = ImageTk.PhotoImage(img)
                
                # Store references
                self.image_references.append(photo)
                
                img_label = tk.Label(frame, image=photo, bg="white")
                img_label.image = photo  # Keep reference
                img_label.pack(side="left", padx=10, pady=10)
                
            except Exception as e:
                # Create placeholder if image fails to load
                placeholder = tk.Label(frame, text="No Image", width=15, height=10, bg="gray")
                placeholder.pack(side="left", padx=10, pady=10)

            # Movie info frame
            info_frame = tk.Frame(frame, bg="white")
            info_frame.pack(side="left", fill="both", expand=True, padx=10)

            tk.Label(info_frame, 
                    text=movie['Title'], 
                    font=("Arial", 14, "bold"), 
                    bg="white").pack(anchor="w")
            
            tk.Label(info_frame, 
                    text=f"Genre: {movie['Genre']}, Rating: {movie['Rating']}, Duration: {movie['Duration']} min", 
                    font=("Arial", 10), 
                    bg="white").pack(anchor="w", pady=(2, 5))
            
            tk.Label(info_frame, 
                    text=f"Actors: {movie['Actors']}", 
                    font=("Arial", 11), 
                    bg="white", 
                    wraplength=700, 
                    justify="left").pack(anchor="w", pady=(0, 5))
            
            tk.Label(info_frame, 
                    text=movie['Description'], 
                    font=("Arial", 11), 
                    bg="white", 
                    wraplength=700, 
                    justify="left").pack(anchor="w")

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)


