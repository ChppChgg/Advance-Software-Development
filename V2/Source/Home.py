"""
Home page implementation
"""
import tkinter as tk
from tkinter import ttk
from Basepage import BasePage

class HomePage(BasePage):
    """Home page showing current and upcoming movies"""
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        
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
        
        # Placeholder for now showing section
        now_showing_frame = tk.LabelFrame(
            content,
            text="NOW SHOWING",
            font=("Arial", 12, "bold"),
            bg="white"
        )
        now_showing_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        placeholder_label = tk.Label(
            now_showing_frame,
            text="Movie listings will be displayed here",
            bg="white"
        )
        placeholder_label.pack(pady=50)
        
        # Placeholder for coming soon section
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