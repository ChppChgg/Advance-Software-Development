import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from Basepage import BasePage
from Database import Database
from datetime import datetime, timedelta
import uuid

class BookingPage(BasePage):
    """Booking page for ticket reservations"""
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Content area
        content = tk.Frame(self.content_frame, bg="white")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Page title
        tk.Label(content,
                 text="Book Movie Tickets",
                 font=("Arial", 16, "bold"),
                 bg="white").pack(anchor="w", pady=(0, 20))
        
        form_frame = tk.Frame(content, bg="white")
        form_frame.pack(fill="both", expand=True)

        # Cinema selection
        tk.Label(form_frame, text="Select Cinema:", font=("Arial", 12), bg="white") \
            .grid(row=0, column=0, sticky="w", pady=10)
        self.cinema_combo = ttk.Combobox(form_frame, font=("Arial", 12), width=50, state="readonly")
        self.cinema_combo.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # Film selection
        tk.Label(form_frame, text="Select Film:", font=("Arial", 12), bg="white") \
            .grid(row=1, column=0, sticky="w", pady=10)
        self.film_combo = ttk.Combobox(form_frame, font=("Arial", 12), width=50, state="readonly")
        self.film_combo.grid(row=1, column=1, pady=10, padx=10, sticky="w")
        self.film_combo.bind("<<ComboboxSelected>>", self.on_film_selected)

        # Date
        tk.Label(form_frame, text="Select Date:", font=("Arial", 12), bg="white") \
            .grid(row=2, column=0, sticky="w", pady=10)
        today = datetime.today()
        self.date_entry = DateEntry(form_frame, font=("Arial", 12), width=30,
                                    background="darkblue", foreground="white",
                                    borderwidth=2, mindate=today,
                                    maxdate=today + timedelta(weeks=1))
        self.date_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        # Time
        tk.Label(form_frame, text="Select Time:", font=("Arial", 12), bg="white") \
            .grid(row=3, column=0, sticky="w", pady=10)
        self.time_combo = ttk.Combobox(form_frame, font=("Arial",12),
                                       width=30, state="readonly")
        self.time_combo.grid(row=3, column=1, pady=10, padx=10, sticky="w")
        self.time_combo.bind("<<ComboboxSelected>>", lambda e: self.calculate_price())

        # Tickets
        tk.Label(form_frame, text="Number of Tickets:", font=("Arial", 12), bg="white") \
            .grid(row=4, column=0, sticky="w", pady=10)
        self.ticket_spinbox = ttk.Spinbox(form_frame, from_=1, to=10,
                                          width=5, font=("Arial",12),
                                          command=self.calculate_price)
        self.ticket_spinbox.grid(row=4, column=1, pady=10, padx=10, sticky="w")
        self.ticket_spinbox.set(1)

        # Seat type
        tk.Label(form_frame, text="Seat Type:", font=("Arial", 12), bg="white") \
            .grid(row=5, column=0, sticky="w", pady=10)
        self.seat_combo = ttk.Combobox(form_frame, font=("Arial",12),
                                       width=15, state="readonly", \
                                       values=["Lower Hall","Upper Gallery","VIP"])
        self.seat_combo.current(0)
        self.seat_combo.grid(row=5, column=1, pady=10, padx=10, sticky="w")
        self.seat_combo.bind("<<ComboboxSelected>>", lambda e: self.calculate_price())

        # Price display
        tk.Label(form_frame, text="Total Price:", font=("Arial", 12), bg="white") \
            .grid(row=6, column=0, sticky="w", pady=10)
        self.price_var = tk.StringVar(value="£0.00")
        self.price_label = tk.Label(form_frame, textvariable=self.price_var,
                                    font=("Arial", 12, "bold"), bg="white")
        self.price_label.grid(row=6, column=1, sticky="w", pady=10)

        # Customer name
        tk.Label(form_frame, text="Full Name:", font=("Arial", 12), bg="white") \
            .grid(row=7, column=0, sticky="w", pady=10)
        self.name_entry = ttk.Entry(form_frame, font=("Arial", 12), width=30)
        self.name_entry.grid(row=7, column=1, pady=10, padx=10, sticky="w")

        # Email
        tk.Label(form_frame, text="Email:", font=("Arial", 12), bg="white") \
            .grid(row=8, column=0, sticky="w", pady=10)
        self.email_entry = ttk.Entry(form_frame, font=("Arial", 12), width=30)
        self.email_entry.grid(row=8, column=1, pady=10, padx=10, sticky="w")

        # Phone
        tk.Label(form_frame, text="Phone Number:", font=("Arial", 12), bg="white") \
            .grid(row=9, column=0, sticky="w", pady=10)
        self.phone_entry = ttk.Entry(form_frame, font=("Arial", 12), width=30)
        self.phone_entry.grid(row=9, column=1, pady=10, padx=10, sticky="w")

        # Proceed
        tk.Button(form_frame, text="Proceed to Seat Selection",
                  font=("Arial",12,"bold"), bg="#1E3F66", fg="white",
                  padx=20, pady=8, command=self.booking_placeholder) \
            .grid(row=10, column=0, columnspan=2, pady=30)

        # Load data
        self.load_cinema_rows()
        self.load_film_rows()

    def load_cinema_rows(self):
        db = Database("horizon_cinemas.db")
        self.cinema_data = db.get_all_cinema_rows()
        values = [f"{c['CinemaName']} | {c['City']}" for c in self.cinema_data] if self.cinema_data else ["No cinemas available"]
        self.cinema_combo['values'] = values
        self.cinema_combo.current(0)

    def load_film_rows(self):
        db = Database("horizon_cinemas.db")
        self.film_data = db.get_all_film_rows()
        values = [f"{f['Title']} | {f['Genre']} | {f['Duration']} min" for f in self.film_data] if self.film_data else ["No films available"]
        self.film_combo['values'] = values
        self.film_combo.current(0)
        # Also preload times
        self.on_film_selected(None)

    def on_film_selected(self, event):
        idx = self.film_combo.current()
        if idx < 0 or idx >= len(self.film_data): return
        film_id = self.film_data[idx]['FilmID']
        screenings = Database("horizon_cinemas.db").get_screenings_by_film(film_id)
        times = [s['StartTime'] for s in screenings]
        self.time_combo['values'] = times if times else ["No screenings available"]
        self.time_combo.current(0)
        self.calculate_price()

    def calculate_price(self):
        # Base ticket price
        price = 5.0
        extraprice = 0.0
        
        # City surcharge
        try:
            city = self.cinema_data[self.cinema_combo.current()]['City']
            if city == 'London':
                price += 5.0
            elif city == 'Bristol':
                price += 1.0
        except:
            pass  # fallback in case cinema combo is empty or selection invalid

        # Time surcharge
        time_str = self.time_combo.get()
        try:
            hour = int(time_str.split(':')[0])
            if 12 <= hour < 17:
                extraprice += 1.0
            elif 17 <= hour <= 23:
                extraprice += 2.0
        except:
            pass  # fallback if time is not selected or invalid

        # Seat type surcharge
        seat = self.seat_combo.get()
        if seat == 'VIP':
            price = (price + price * 0.2)*1.2
        elif seat == 'Upper Gallery':
            price = (price + price * 0.2)

        # Ticket quantity
        try:
            qty = int(self.ticket_spinbox.get())
        except:
            qty = 1

        total = ((price + extraprice) * qty)
        self.price_var.set(f"£{total:.2f}")

    def booking_placeholder(self):
        try:
            db = Database("horizon_cinemas.db")

            quantity = int(self.ticket_spinbox.get())

            name = self.name_entry.get().strip()
            email = self.email_entry.get().strip()
            phone = self.phone_entry.get().strip()

            # Get selected cinema and film
            cinema_idx = self.cinema_combo.current()
            cinema_id = self.cinema_data[cinema_idx]['CinemaID']

            film_idx = self.film_combo.current()
            film_id = self.film_data[film_idx]['FilmID']

            # Get selected date and time
            show_date = self.date_entry.get_date().strftime("%Y-%m-%d")
            show_time = self.time_combo.get()

            # Find matching screening ID
            # Find matching screening ID
            screenings = db.get_screenings_by_film(film_id)
            matching_screening = next(
                (s for s in screenings if s['StartTime'] == show_time), None
            )
            if not matching_screening:
                messagebox.showerror("Error", "No matching screening found.")
                return

            screening_id = matching_screening['ScreeningID']

            # Total price
            total_price = float(self.price_var.get().replace("£", ""))
            cancellationfee = (total_price/2)

            # Generate unique booking reference
            booking_ref = str(uuid.uuid4())[:8].upper()  # Simple unique code, e.g., 'A3F9D2B1'

            bookingdatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            status = 'active'

            customer_id = db.insert_customer(name, email, phone)

            # Insert booking
            db.insert_booking(
                customer_id = customer_id,
                cinema_id=cinema_id,
                screening_id=screening_id,
                booking_ref=booking_ref,
                total_price=total_price,
                cancellationfee=cancellationfee,
                quantity=quantity,
                bookingdatetime=bookingdatetime,
                status=status
            )

            messagebox.showinfo("Success", f"Booking successful!\nReference: {booking_ref}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save booking:\n{e}")
