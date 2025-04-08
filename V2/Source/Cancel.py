"""
Cancellation page functions
"""
import tkinter as tk
from tkinter import ttk, messagebox
from Basepage import BasePage

class CancellationPage(BasePage):
    """Page for viewing and cancelling bookings"""
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        
        # Content area
        content = tk.Frame(self.content_frame, bg="white")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Page title
        page_title = tk.Label(
            content,
            text="My Bookings",
            font=("Arial", 16, "bold"),
            bg="white"
        )
        page_title.pack(anchor="w", pady=(0, 20))
        
        # Bookings list frame
        bookings_frame = tk.Frame(content, bg="white")
        bookings_frame.pack(fill="both", expand=True)
        
        # Treeview for bookings
        columns = ("booking_id", "film", "date", "time", "seats", "status")
        self.bookings_tree = ttk.Treeview(bookings_frame, columns=columns, show="headings")
        
        # Define headings
        self.bookings_tree.heading("booking_id", text="Booking Ref")
        self.bookings_tree.heading("film", text="Film")
        self.bookings_tree.heading("date", text="Date")
        self.bookings_tree.heading("time", text="Time")
        self.bookings_tree.heading("seats", text="Seats")
        self.bookings_tree.heading("status", text="Status")
        
        # Define column widths
        self.bookings_tree.column("booking_id", width=100)
        self.bookings_tree.column("film", width=200)
        self.bookings_tree.column("date", width=100)
        self.bookings_tree.column("time", width=100)
        self.bookings_tree.column("seats", width=100)
        self.bookings_tree.column("status", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(bookings_frame, orient="vertical", command=self.bookings_tree.yview)
        self.bookings_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        scrollbar.pack(side="right", fill="y")
        self.bookings_tree.pack(fill="both", expand=True)
        
        # Placeholder data
        self.bookings_tree.insert("", "end", values=("No bookings found", "", "", "", "", ""))
        
        # Buttons frame
        buttons_frame = tk.Frame(content, bg="white")
        buttons_frame.pack(fill="x", pady=20)
        
        # Cancel button
        cancel_button = tk.Button(
            buttons_frame,
            text="Cancel Selected Booking",
            font=("Arial", 12),
            bg="#DF4759",
            fg="white",
            padx=15,
            pady=5,
            command=self.cancel_placeholder
        )
        cancel_button.pack(side="left", padx=10)
        
        # Refresh button
        refresh_button = tk.Button(
            buttons_frame,
            text="Refresh Bookings",
            font=("Arial", 12),
            bg="#1E3F66",
            fg="white",
            padx=15,
            pady=5,
            command=self.refresh_placeholder
        )
        refresh_button.pack(side="left", padx=10)
        
    def cancel_placeholder(self):
        """Placeholder for cancellation functionality"""
        messagebox.showinfo("Cancel", "Cancellation functionality will be implemented later")
    
    def refresh_placeholder(self):
        """Placeholder for refresh functionality"""
        messagebox.showinfo("Refresh", "Refresh functionality will be implemented later")