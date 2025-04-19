import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from Basepage import BasePage
from Database import Database
from datetime import datetime, timedelta

class BookingPage(BasePage):
    """Booking page for ticket reservations"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Content area
        content = tk.Frame(self.content_frame, bg="white")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Page title
        tk.Label(
            content,
            text="Book Movie Tickets",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(anchor="w", pady=(0, 20))
        
        # Booking form frame
        form_frame = tk.Frame(content, bg="white")
        form_frame.pack(fill="both", expand=True)

        # Cinema selection (does not affect films)
        tk.Label(
            form_frame,
            text="Select Cinema:",
            font=("Arial", 12),
            bg="white"
        ).grid(row=0, column=0, sticky="w", pady=10)

        self.cinema_combo = ttk.Combobox(
            form_frame,
            font=("Arial", 12),
            width=50,
            state="readonly"
        )
        self.cinema_combo.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # Film selection (independent of cinema)
        tk.Label(
            form_frame,
            text="Select Film:",
            font=("Arial", 12),
            bg="white"
        ).grid(row=1, column=0, sticky="w", pady=10)
        
        self.film_combo = ttk.Combobox(
            form_frame,
            font=("Arial", 12),
            width=50,
            state="readonly"
        )
        self.film_combo.grid(row=1, column=1, pady=10, padx=10, sticky="w")
        self.film_combo.bind("<<ComboboxSelected>>", self.on_film_selected)

        # Date selection
        tk.Label(
            form_frame,
            text="Select Date:",
            font=("Arial", 12),
            bg="white"
        ).grid(row=2, column=0, sticky="w", pady=10)
        
        today = datetime.today()
        one_week_later = today + timedelta(weeks=1)
        
        self.date_entry = DateEntry(
            form_frame,
            font=("Arial", 12),
            width=30,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            mindate=today,
            maxdate=one_week_later
        )
        self.date_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")
            
        # Time selection
        tk.Label(
            form_frame,
            text="Select Time:",
            font=("Arial", 12),
            bg="white"
        ).grid(row=3, column=0, sticky="w", pady=10)
        
        self.time_combo = ttk.Combobox(
            form_frame,
            font=("Arial",12),
            width=30,
            state="readonly"
        )
        self.time_combo.grid(row=3, column=1, pady=10, padx=10, sticky="w")
        self.time_combo['values'] = ["Select a time..."]
        self.time_combo.current(0)
        
        # Ticket quantity
        tk.Label(
            form_frame,
            text="Number of Tickets:",
            font=("Arial", 12),
            bg="white"
        ).grid(row=4, column=0, sticky="w", pady=10)
        
        self.ticket_spinbox = ttk.Spinbox(
            form_frame,
            from_=1,
            to=10,
            width=5,
            font=("Arial", 12)
        )
        self.ticket_spinbox.grid(row=4, column=1, pady=10, padx=10, sticky="w")
        self.ticket_spinbox.set(1)
        
        # Seat type
        tk.Label(
            form_frame,
            text="Seat Type:",
            font=("Arial", 12),
            bg="white"
        ).grid(row=5, column=0, sticky="w", pady=10)
        
        self.seat_combo = ttk.Combobox(
            form_frame,
            font=("Arial", 12),
            width=15,
            state="readonly"
        )
        self.seat_combo.grid(row=5, column=1, pady=10, padx=10, sticky="w")
        self.seat_combo['values'] = ["Lower Hall", "Upper Gallery", "VIP"]
        self.seat_combo.current(0)
        
        # Proceed button
        tk.Button(
            form_frame,
            text="Proceed to Seat Selection",
            font=("Arial", 12, "bold"),
            bg="#1E3F66",
            fg="white",
            padx=20,
            pady=8,
            command=self.booking_placeholder
        ).grid(row=6, column=0, columnspan=2, pady=30)

        # Load data
        self.load_cinema_rows()
        self.load_film_rows()

    def load_cinema_rows(self):
        """Load cinemas into the cinema combobox"""
        db = Database("horizon_cinemas.db")
        self.cinema_data = db.get_all_cinema_rows()
        if self.cinema_data:
            formatted = [f"{cinema['CinemaName']} | {cinema['City']}" for cinema in self.cinema_data]
            self.cinema_combo['values'] = formatted
            self.cinema_combo.current(0)
        else:
            self.cinema_combo['values'] = ["No cinemas available"]
            self.cinema_combo.current(0)

    def load_film_rows(self):
        """Load detailed film rows into the combobox with formatted display"""
        db = Database("horizon_cinemas.db")
        self.film_data = db.get_all_film_rows()
        if self.film_data:
            formatted = [f"{film['Title']} | {film['Genre']} | {film['Duration']} min" for film in self.film_data]
            self.film_combo['values'] = formatted
            self.film_combo.current(0)
        else:
            self.film_combo['values'] = ["No films available"]
            self.film_combo.current(0)

    def on_film_selected(self, event):
        """When a film is chosen, fetch its screening times and fill time_combo."""
        idx = self.film_combo.current()
        if idx < 0 or idx >= len(self.film_data):
            self.time_combo['values'] = ["Select a time..."]
            self.time_combo.current(0)
            return

        film_id = self.film_data[idx]['FilmID']
        screenings = Database("horizon_cinemas.db").get_screenings_by_film(film_id)
        times = [s['StartTime'] for s in screenings]

        if times:
            self.time_combo['values'] = times
            self.time_combo.current(0)
        else:
            self.time_combo['values'] = ["No screenings available"]
            self.time_combo.current(0)

    def booking_placeholder(self):
        """Placeholder for booking functionality"""
        messagebox.showinfo("Booking", "Booking functionality will be implemented later")