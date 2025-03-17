import tkinter as tk
from tkinter import ttk, messagebox
from BasePage import BasePage

class BookingPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        
        # Create booking form
        booking_frame = tk.Frame(self.content, bg="white", padx=30, pady=30)
        booking_frame.place(relx=0.5, rely=0.4, anchor="center")
        booking_title = tk.Label(booking_frame, text="Booking", font=("Helvetica", 24), bg="white")
        booking_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        film_label = tk.Label(booking_frame, text="Film:", bg="white")
        film_label.grid(row=1, column=0, sticky="w", pady=5)
        self.film_var = tk.StringVar()
        self.film_dropdown = ttk.Combobox(booking_frame, textvariable=self.film_var, 
                                        state="readonly", width=30)
        self.film_dropdown.grid(row=1, column=1, pady=5)
        date_label = tk.Label(booking_frame, text="Date:", bg="white")
        date_label.grid(row=2, column=0, sticky="w", pady=5)
        
        # Create a frame for date selection (in a real app, use a calendar widget)
        date_frame = tk.Frame(booking_frame, bg="white")
        date_frame.grid(row=2, column=1, sticky="w", pady=5)
        
        # Simulate date selection with dropdown menus
        self.day_var = tk.StringVar(value="1")
        day_dropdown = ttk.Combobox(date_frame, textvariable=self.day_var, 
                                 values=[str(i) for i in range(1, 32)], width=5)
        day_dropdown.pack(side="left", padx=(0, 5))
        
        self.month_var = tk.StringVar(value="January")
        month_dropdown = ttk.Combobox(date_frame, textvariable=self.month_var, 
                                   values=["January", "February", "March", "April", 
                                         "May", "June", "July", "August", 
                                         "September", "October", "November", "December"], 
                                   width=10)
        month_dropdown.pack(side="left", padx=5)
        
        self.year_var = tk.StringVar(value="2025")
        year_dropdown = ttk.Combobox(date_frame, textvariable=self.year_var, 
                                  values=["2025", "2026"], width=6)
        year_dropdown.pack(side="left", padx=5)
        
        time_label = tk.Label(booking_frame, text="Show Time:", bg="white")
        time_label.grid(row=3, column=0, sticky="w", pady=5)
        
        self.time_var = tk.StringVar()
        self.time_dropdown = ttk.Combobox(booking_frame, textvariable=self.time_var, 
                                        values=["10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM", "10:00 PM"], 
                                        state="readonly", width=30)
        self.time_dropdown.grid(row=3, column=1, pady=5)
        
        ticket_label = tk.Label(booking_frame, text="Ticket Type:", bg="white")
        ticket_label.grid(row=4, column=0, sticky="w", pady=5)
        
        self.ticket_var = tk.StringVar(value="Standard ($10)")
        ticket_dropdown = ttk.Combobox(booking_frame, textvariable=self.ticket_var, 
                                    values=["Standard ($10)", "Premium ($15)", "VIP ($20)"], 
                                    state="readonly", width=30)
        ticket_dropdown.grid(row=4, column=1, pady=5)
        
        quantity_label = tk.Label(booking_frame, text="Number of Tickets:", bg="white")
        quantity_label.grid(row=5, column=0, sticky="w", pady=5)
        
        self.quantity_var = tk.StringVar(value="1")
        quantity_spinbox = tk.Spinbox(booking_frame, from_=1, to=10, textvariable=self.quantity_var, width=5)
        quantity_spinbox.grid(row=5, column=1, sticky="w", pady=5)
        
        continue_button = tk.Button(booking_frame, text="Continue to Seat Selection", 
                                 command=self.proceed_booking, bg="#ff4500", fg="white")
        continue_button.grid(row=6, column=1, sticky="e", pady=20)
    
    def on_show(self):
        """Update film dropdown when page is shown"""
        # Check if user is logged in
        if not self.controller.current_user:
            messagebox.showerror("Access Denied", "Please log in to book tickets.")
            self.controller.show_frame("LoginPage")
            return
        # Get movie titles for dropdown
        movies = [m for m in self.controller.movies if m["status"] == "now_showing"]
        movie_titles = [m["title"] for m in movies]
        self.film_dropdown['values'] = movie_titles
        
        # If a movie was selected from home page, set it
        if hasattr(self.controller, 'selected_movie') and self.controller.selected_movie:
            self.film_var.set(self.controller.selected_movie["title"])
        elif movie_titles:
            self.film_var.set(movie_titles[0])
    
    def proceed_booking(self):
        """Handle booking submission"""
        # In a real app, save booking details to database
        # and proceed to seat selection
        
        if not self.film_var.get():
            messagebox.showerror("Error", "Please select a film.")
            return
        
        date_str = f"{self.day_var.get()} {self.month_var.get()} {self.year_var.get()}"
        
        booking_details = f"Film: {self.film_var.get()}\n" \
                         f"Date: {date_str}\n" \
                         f"Time: {self.time_var.get()}\n" \
                         f"Ticket Type: {self.ticket_var.get()}\n" \
                         f"Quantity: {self.quantity_var.get()}"
        
        messagebox.showinfo("Booking Details", booking_details)
        # In a complete app, navigate to seat selection screen