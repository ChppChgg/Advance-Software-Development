"""
Cancellation page functions
"""
import tkinter as tk
from tkinter import ttk, messagebox
from Basepage import BasePage
import sqlite3
from Database import Database
from datetime import datetime

#Harry Elson, 23021935
#Matt Nogodula, 23015215
#Jerry Lin, 23024553

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
            text="Bookings",
            font=("Arial", 16, "bold"),
            bg="white"
        )
        page_title.pack(anchor="w", pady=(0, 20))
        
        # Bookings list frame
        bookings_frame = tk.Frame(content, bg="white")
        bookings_frame.pack(fill="both", expand=True)
        
        # Treeview for bookings
        columns = ("booking_id", "film", "date", "time", "seats", "email", "cinema", "status")
        self.bookings_tree = ttk.Treeview(bookings_frame, columns=columns, show="headings")
        
        # Define headings
        self.bookings_tree.heading("booking_id", text="Booking Ref")
        self.bookings_tree.heading("film", text="Film")
        self.bookings_tree.heading("date", text="Date")
        self.bookings_tree.heading("time", text="Time")
        self.bookings_tree.heading("seats", text="Seats")
        self.bookings_tree.heading("email", text="Email")
        self.bookings_tree.heading("cinema", text="Cinema")
        self.bookings_tree.heading("status", text="Status")
        
        # Define column widths
        self.bookings_tree.column("booking_id", width=100)
        self.bookings_tree.column("film", width=180)
        self.bookings_tree.column("date", width=100)
        self.bookings_tree.column("time", width=80)
        self.bookings_tree.column("seats", width=60)
        self.bookings_tree.column("email", width=180)
        self.bookings_tree.column("cinema", width=120)
        self.bookings_tree.column("status", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(bookings_frame, orient="vertical", command=self.bookings_tree.yview)
        self.bookings_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        scrollbar.pack(side="right", fill="y")
        self.bookings_tree.pack(fill="both", expand=True)
        
        # Placeholder data
        self.bookings_tree.insert("", "end", values=("No bookings found", "", "", "", "", "", "", ""))
        
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

    
    def load_user_bookings(self):
        try:
            db = Database("horizon_cinemas.db")
            
            username_display = self.username_label.cget("text")
            username = username_display.replace("Welcome, ", "").strip()
            
            # Get user role and cinema ID
            user_role = db.get_user_role_by_username(username)
            cinema_id = db.get_cinema_id_by_username(username)
            
            if not cinema_id and user_role != "Admin" and user_role != "Manager":
                messagebox.showerror("Error", "No cinema assigned to this user.")
                return
            
            # Get bookings based on role and cinema assignment
            if user_role in ["Admin", "Manager"]:
                # Admins and managers automatically see all bookings across all cinemas
                bookings = db.get_bookings(cinema_id=None, include_details=True)
            else:
                # Staff can only see bookings from their cinema
                bookings = db.get_bookings(cinema_id=cinema_id, include_details=True)
            
            # Clear old bookings in Treeview
            self.bookings_tree.delete(*self.bookings_tree.get_children())
            
            if not bookings:
                self.bookings_tree.insert("", "end", values=("No bookings found", "", "", "", "", "", "", ""))
            else:
                for b in bookings:
                    self.bookings_tree.insert("", "end", values=(
                        b["BookingReference"],
                        b["Title"],
                        b["BookingDate"],
                        b["StartTime"],
                        b["SeatCount"],
                        b["UserEmail"],
                        b["CinemaName"],
                        b["Status"]
                    ))
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bookings:\n{e}")

    def cancel_placeholder(self):
        selected_item = self.bookings_tree.focus()
        if not selected_item:
            messagebox.showwarning("No selection", "Please select a booking to cancel.")
            return

        booking_ref = self.bookings_tree.item(selected_item, "values")[0]

        try:
            db = Database("horizon_cinemas.db")

            # Fetch booking date and cancellation fee
            booking_info = db.get_booking_info_by_reference(booking_ref)
            if not booking_info:
                messagebox.showerror("Error", "Could not find booking details.")
                return

            booking_date_str = booking_info.get("BookingDate")
            cancellation_fee = booking_info.get("CancellationFee")
            status = booking_info.get("Status")

            if not booking_date_str or cancellation_fee is None:
                messagebox.showerror("Error", "Missing booking date or cancellation fee.")
                return

            # Prevent cancellation if it's for today's date
            booking_date = datetime.strptime(booking_date_str, "%Y-%m-%d").date()
            today = datetime.today().date()

            if status == "cancelled":
                messagebox.showinfo("Already Cancelled", "This booking has already been cancelled.")
                return

            if booking_date == today:
                messagebox.showwarning("Too Late", "You cannot cancel a booking on the day of the screening.")
                return

            # Ask for confirmation and display fee
            confirm = messagebox.askyesno(
                "Confirm Cancellation",
                f"Are you sure you want to cancel booking {booking_ref}?\n"
                f"A cancellation fee of £{cancellation_fee:.2f} will be applied."
            )
            if not confirm:
                return

            # Proceed with cancellation
            success = db.cancel_booking_by_reference(booking_ref)
            if success:
                messagebox.showinfo("Cancelled", "Booking cancelled successfully.")
                self.load_user_bookings()
            else:
                messagebox.showerror("Error", "Failed to cancel booking.")

        except Exception as e:
            messagebox.showerror("Error", f"Cancellation failed:\n{e}")

    def refresh_placeholder(self):
       self.load_user_bookings()