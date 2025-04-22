"""
Home page implementation
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Basepage import BasePage

#Harry Elson, 23021935
#Matt Nogodula, 23015215
#Jerry Lin, 23024553

class HomePage(BasePage):
    """Home page showing current and upcoming movies"""
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        self.controller = controller

        # Content area
        content = tk.Frame(self.content_frame, bg="white")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Page title
        page_title = tk.Label(
            content,
            text="Welcome to Horizon Cinemas",
            font=("Arial", 16, "bold"),
            bg="white"
        )
        page_title.pack(anchor="w", pady=(0, 20))

        # NOW SHOWING section
        now_showing_frame = tk.LabelFrame(
            content,
            text="NOW SHOWING",
            font=("Arial", 12, "bold"),
            bg="white"
        )
        now_showing_frame.pack(fill="x", pady=(0, 20))

        # Load and display images
        image_files = [
            ("V2/Source/images/minecraft.jfif", "A Minecraft Movie"),
            ("V2/Source/images/amatuar.jpg", "The Amateur"),
            ("V2/Source/images/unicorn.jfif", "Death of a Unicorn"),
            ("V2/Source/images/drop.jfif", "Drop"),
            ("V2/Source/images/starwars.jfif", "Starwars Episode III")
        ]

        self.images = []  # Keep references to PhotoImage objects

        for img_path, movie_name in image_files:
            try:
                img = Image.open(img_path)
                img = img.resize((150, 220))  # Resize for thumbnails
                photo = ImageTk.PhotoImage(img)
                self.images.append(photo)

                # Create a frame for each movie
                movie_frame = tk.Frame(now_showing_frame, bg="white")
                movie_frame.pack(side="left", padx=10)

                # Add image
                img_label = tk.Label(movie_frame, image=photo, cursor="hand2", bg="white")
                img_label.pack()


                # Add label under image
                title_label = tk.Label(movie_frame, text=movie_name, bg="white", font=("Arial", 10, "bold"))
                title_label.pack(pady=5)
            except Exception as e:
                print(f"Error loading {img_path}: {e}")

        # COMING SOON section (left as placeholder)
        coming_soon_frame = tk.LabelFrame(
            content,
            text="COMING SOON",
            font=("Arial", 12, "bold"),
            bg="white"
        )
        coming_soon_frame.pack(fill="both", expand=True)

        placeholder_label2 = tk.Label(
            coming_soon_frame,
            text="Upcoming movie listings will be displayed here",
            bg="white"
        )
        placeholder_label2.pack(pady=50)


