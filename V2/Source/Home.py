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

        # Store content frame reference for refresh method
        self.content = content
        
        # Create the page content
        self.create_page_content()
        
    def create_page_content(self):
        """Create the page content - separated to allow refreshing"""
        # Clear existing widgets except title
        for widget in self.content.winfo_children()[1:]:
            widget.destroy()
            
        # NOW SHOWING section
        now_showing_frame = tk.LabelFrame(
            self.content,
            text="NOW SHOWING",
            font=("Arial", 12, "bold"),
            bg="white"
        )
        now_showing_frame.pack(fill="x", pady=(0, 20))

        # Load and display images
        image_files = [
            ("V2/Source/images/aminecraftmovie.jfif", "A Minecraft Movie"),
            ("V2/Source/images/theamateur.jfif", "The Amateur"),
            ("V2/Source/images/deathofaunicorn.jfif", "Death of a Unicorn"),
            ("V2/Source/images/drop.jfif", "Drop"),
            ("V2/Source/images/starwarsepisodeiiirevengeofthesith20thanniversary.jfif", "Starwars Episode III")
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

        # USER INFO section
        user_info_frame = tk.LabelFrame(
            self.content,
            text="USER INFO",
            font=("Arial", 12, "bold"),
            bg="white"
        )
        user_info_frame.pack(fill="both", expand=True, pady=(10, 0))

        # Get user information from controller
        user_name = self.controller.get_user_name() if hasattr(self.controller, 'get_user_name') else "N/A"
        user_role = self.controller.get_user_role() if hasattr(self.controller, 'get_user_role') else "N/A"

        # Create frame for user info content
        user_details_frame = tk.Frame(user_info_frame, bg="white", pady=15, padx=15)
        user_details_frame.pack(fill="both", anchor="w")

        # Name label
        name_label = tk.Label(
            user_details_frame,
            text=f"Name: {user_name}",
            font=("Arial", 11),
            bg="white",
            anchor="w"
        )
        name_label.pack(fill="x", pady=2)

        # Role label
        role_label = tk.Label(
            user_details_frame,
            text=f"Role: {user_role}",
            font=("Arial", 11),
            bg="white",
            anchor="w"
        )
        role_label.pack(fill="x", pady=2)

        # Cinema label - conditional display based on role
        if user_role != "N/A":  # Only show cinema info if logged in
            cinema_text = ""
            role_lower = user_role.lower()

            if role_lower == "staff":
                if hasattr(self.controller, 'get_user_cinema'):
                    user_cinema = self.controller.get_user_cinema()
                    cinema_text = f"Cinema: {user_cinema if user_cinema else 'N/A'}"
                else:
                    cinema_text = "Cinema: N/A" # Fallback if method missing
            elif role_lower in ["manager", "admin"]:
                cinema_text = "Cinema: ALL"

            # Only create the label if there's text to display
            if cinema_text:
                cinema_label = tk.Label(
                    user_details_frame,
                    text=cinema_text,
                    font=("Arial", 11),
                    bg="white",
                    anchor="w"
                )
                cinema_label.pack(fill="x", pady=2)

    def refresh(self):
        """Refresh the page content when user logs in/out"""
        self.create_page_content()


