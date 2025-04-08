"""
booking page functions
"""
import tkinter as tk
from tkinter import ttk, messagebox
from Basepage import BasePage

class BookingPage(BasePage):
    """Booking page for ticket reservations"""
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        
        # Content area
        content = tk.Frame(self.content_frame, bg="white")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Page title
        page_title = tk.Label(
            content,
            text="Book Movie Tickets",
            font=("Arial", 16, "bold"),
            bg="white"
        )
        page_title.pack(anchor="w", pady=(0, 20))
        
        # Booking form frame
        form_frame = tk.Frame(content, bg="white")
        form_frame.pack(fill="both", expand=True)
        
        # Film selection
        film_label = tk.Label(
            form_frame,
            text="Select Film:",
            font=("Arial", 12),
            bg="white"
        )
        film_label.grid(row=0, column=0, sticky="w", pady=10)
        
        self.film_combo = ttk.Combobox(
            form_frame,
            font=("Arial", 12),
            width=30,
            state="readonly"
        )
        self.film_combo.grid(row=0, column=1, pady=10, padx=10, sticky="w")
        self.film_combo['values'] = ["Select a film..."]  # Will be populated later
        self.film_combo.current(0)
        
        # Date selection
        date_label = tk.Label(
            form_frame,
            text="Select Date:",
            font=("Arial", 12),
            bg="white"
        )
        date_label.grid(row=1, column=0, sticky="w", pady=10)
        
        self.date_combo = ttk.Combobox(
            form_frame,
            font=("Arial", 12),
            width=30,
            state="readonly"
        )
        self.date_combo.grid(row=1, column=1, pady=10, padx=10, sticky="w")
        self.date_combo['values'] = ["Select a date..."]  # Will be populated later
        self.date_combo.current(0)
        
        # Time selection
        time_label = tk.Label(
            form_frame,
            text="Select Time:",
            font=("Arial", 12),
            bg="white"
        )
        time_label.grid(row=2, column=0, sticky="w", pady=10)
        
        self.time_combo = ttk.Combobox(
            form_frame,
            font=("Arial", 12),
            width=30,
            state="readonly"
        )
        self.time_combo.grid(row=2, column=1, pady=10, padx=10, sticky="w")
        self.time_combo['values'] = ["Select a time..."]  # Will be populated later
        self.time_combo.current(0)
        
        # Ticket quantity
        ticket_label = tk.Label(
            form_frame,
            text="Number of Tickets:",
            font=("Arial", 12),
            bg="white"
        )
        ticket_label.grid(row=3, column=0, sticky="w", pady=10)
        
        self.ticket_spinbox = ttk.Spinbox(
            form_frame,
            from_=1,
            to=10,
            width=5,
            font=("Arial", 12)
        )
        self.ticket_spinbox.grid(row=3, column=1, pady=10, padx=10, sticky="w")
        self.ticket_spinbox.set(1)
        
        # Seat type
        seat_label = tk.Label(
            form_frame,
            text="Seat Type:",
            font=("Arial", 12),
            bg="white"
        )
        seat_label.grid(row=4, column=0, sticky="w", pady=10)
        
        self.seat_combo = ttk.Combobox(
            form_frame,
            font=("Arial", 12),
            width=15,
            state="readonly"
        )
        self.seat_combo.grid(row=4, column=1, pady=10, padx=10, sticky="w")
        self.seat_combo['values'] = ["Lower Hall", "Upper Gallery", "VIP"]
        self.seat_combo.current(0)
        
        # Proceed button
        proceed_button = tk.Button(
            form_frame,
            text="Proceed to Seat Selection",
            font=("Arial", 12, "bold"),
            bg="#1E3F66",
            fg="white",
            padx=20,
            pady=8,
            command=self.booking_placeholder
        )
        proceed_button.grid(row=5, column=0, columnspan=2, pady=30)
        
    def booking_placeholder(self):
        """Placeholder for booking functionality"""
        messagebox.showinfo("Booking", "Booking functionality will be implemented later")