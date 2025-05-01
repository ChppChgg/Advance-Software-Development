"""
Admin page 
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from Basepage import BasePage
from Database import Database
import sqlite3
import sqlite3
import csv
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Harry Elson, 23021935
#Matt Nogodula, 23015215
#Jerry Lin, 23024553

class AdminPage(BasePage):
    """Admin page for cinema management"""
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        
        # Create database instance for this page
        self.db = Database()
        
        # Content area
        content = tk.Frame(self.content_frame, bg="white")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Page title
        page_title = tk.Label(
            content,
            text="Cinema Admin Dashboard",
            font=("Arial", 16, "bold"),
            bg="white"
        )
        page_title.pack(anchor="w", pady=(0, 20))
        
        # Tabs for different Admin functions
        tab_control = ttk.Notebook(content)
        # Screenings tab
        screenings_tab = ttk.Frame(tab_control)
        tab_control.add(screenings_tab, text="Screenings")
        films_tab = ttk.Frame(tab_control)
        tab_control.add(films_tab, text="Films")
        reports_tab = ttk.Frame(tab_control)
        tab_control.add(reports_tab, text="Reports")
        
        tab_control.pack(expand=1, fill="both")
        self.setup_screenings_tab(screenings_tab)
        self.setup_films_tab(films_tab)
        self.setup_reports_tab(reports_tab)

    def setup_screenings_tab(self, parent):
        """Set up the screenings management tab"""
        # Main frame for the tab content
        self.screenings_frame = tk.Frame(parent)
        self.screenings_frame.pack(fill="both", expand=True)
        self.show_cinema_selection_interface() #Open up on cinema's tab

    def show_cinema_selection_interface(self):
        """Show interface for selecting cinemas before showing screenings"""
        for widget in self.screenings_frame.winfo_children(): # clear UI 
            widget.destroy()
        #Show cinema tab title
        title_label = tk.Label(
            self.screenings_frame, 
            text="Select a Cinema to View Screenings",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Get all cinemas from the database
        try:
            conn = self.db.connect() # open connection
            cursor = conn.cursor()
            cursor.execute("SELECT CinemaID, CinemaName FROM Cinemas ORDER BY CinemaName") #get data for cinema
            cinemas = cursor.fetchall() #fetches data from query
            self.db.close() #close connection
            
            if not cinemas: #error handling incase no data exists
                no_cinemas_label = tk.Label(
                    self.screenings_frame,
                    text="No cinemas found in the database.",
                    font=("Arial", 12)
                )
                no_cinemas_label.pack(pady=20)
                return
            
            #allow scrolling
            container_frame = tk.Frame(self.screenings_frame)
            container_frame.pack(fill="both", expand=True, padx=10, pady=10)
            # Create a canvas for scrolling
            canvas = tk.Canvas(container_frame)
            scrollbar = ttk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
            buttons_frame = tk.Frame(canvas) #buttons for cinema list
            
            #Link scroll bar and canvas holding buttons
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Add the buttons frame to the canvas
            canvas_window = canvas.create_window((0, 0), window=buttons_frame, anchor="nw")
            
            #button to show all cinema listings
            all_cinemas_btn = tk.Button(
                buttons_frame,
                text="View All Cinemas",
                width=25,
                font=("Arial", 11),
                command=lambda: self.show_screenings_for_cinema(None)
            )
            all_cinemas_btn.pack(pady=8)
            
            # Create buttons for each cinema
            for cinema in cinemas:
                cinema_btn = tk.Button(
                    buttons_frame,
                    text=cinema["CinemaName"], #gets cinema name from db
                    width=25,
                    font=("Arial", 11),
                    command=lambda cid=cinema["CinemaID"], cname=cinema["CinemaName"]: self.show_screenings_for_cinema(cid, cname)
                )
                cinema_btn.pack(pady=8)
            
            # Update the when new cinema's are insertedd
            def configure_scroll_region(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.itemconfig(canvas_window, width=canvas.winfo_width())
            buttons_frame.bind("<Configure>", configure_scroll_region)
            
            #responsive button design
            def resize_canvas(event):
                canvas.itemconfig(canvas_window, width=event.width)
            
            canvas.bind("<Configure>", resize_canvas)
            
            # Enable scrolling with mouse wheel
            def on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            canvas.bind_all("<MouseWheel>", on_mousewheel)
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load cinemas: {e}")

    def show_screenings_for_cinema(self, cinema_id, cinema_name=None):
        """Show screenings for the selected cinema"""
        # Clear the screenings frame
        for widget in self.screenings_frame.winfo_children():
            widget.destroy()
        # Create a header with back button and cinema name
        header_frame = tk.Frame(self.screenings_frame)
        header_frame.pack(fill="x", pady=(10, 20))
        
        # Back button
        back_btn = tk.Button(
            header_frame,
            text="← Back to Cinema Selection",
            command=self.show_cinema_selection_interface
        )
        back_btn.pack(side="left", padx=10)
        
        # Title showing which cinema we're viewing
        title_text = "All Screenings" if cinema_id is None else f"Screenings for {cinema_name}"
        title_label = tk.Label(
            header_frame,
            text=title_text,
            font=("Arial", 12, "bold")
        )
        title_label.pack(side="right", padx=10)
        
        # Screenings list frame
        list_frame = tk.Frame(self.screenings_frame)
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Screenings treeview - Add cinema column
        columns = ("id", "cinema", "film", "screen", "start_time", "end_time", "seats")
        self.screenings_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings for the table
        self.screenings_tree.heading("id", text="ID")
        self.screenings_tree.heading("cinema", text="Cinema")
        self.screenings_tree.heading("film", text="Film")
        self.screenings_tree.heading("screen", text="Screen")
        self.screenings_tree.heading("start_time", text="Start Time")
        self.screenings_tree.heading("end_time", text="End Time")
        self.screenings_tree.heading("seats", text="Total Seats")
        
        # Define column 
        self.screenings_tree.column("id", width=50)
        self.screenings_tree.column("cinema", width=150)
        self.screenings_tree.column("film", width=200)
        self.screenings_tree.column("screen", width=80)
        self.screenings_tree.column("start_time", width=100)
        self.screenings_tree.column("end_time", width=100)
        self.screenings_tree.column("seats", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.screenings_tree.yview)
        self.screenings_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        scrollbar.pack(side="right", fill="y")
        self.screenings_tree.pack(fill="both", expand=True)
        
        # Load screenings data for the selected cinema
        self.load_screenings_data(cinema_id)
        
        # Control frame
        control_frame = tk.Frame(self.screenings_frame)
        control_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        # Add screening button
        add_button = tk.Button(
            control_frame,
            text="Add Screening",
            width=15,
            command=self.show_add_screening_dialog
        )
        add_button.pack(pady=5)
        
        # Edit screening button
        edit_button = tk.Button(
            control_frame,
            text="Edit Screening",
            width=15,
            command=self.show_edit_screening_dialog
        )
        edit_button.pack(pady=5)
        
        # Delete screening button
        delete_button = tk.Button(
            control_frame,
            text="Delete Screening",
            width=15,
            command=self.delete_screening
        )
        delete_button.pack(pady=5)
        
        # Add refresh button
        refresh_button = tk.Button(
            control_frame,
            text="Refresh List",
            width=15,
            command=lambda: self.load_screenings_data(cinema_id)
        )
        refresh_button.pack(pady=5)

    def load_screenings_data(self, cinema_id=None):
        """Load screenings data from database into treeview"""
        for item in self.screenings_tree.get_children():
            self.screenings_tree.delete(item)
            
        try:
            # Connect to database - use local db instance
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Base query with cinema name from Screens-Cinemas relationship
            query = """
                SELECT s.ScreeningID, f.Title, scr.ScreenNumber, s.StartTime, 
                      s.EndTime, s.TotalSeats, c.CinemaName, c.CinemaID
                FROM Screenings s
                JOIN Films f ON s.FilmID = f.FilmID
                JOIN Screens scr ON s.ScreenID = scr.ScreenID
                LEFT JOIN Cinemas c ON scr.CinemaID = c.CinemaID
            """
            
            # Add filter for specific cinema if provided
            if cinema_id:
                query += " WHERE c.CinemaID = ?"
                cursor.execute(query + " ORDER BY s.StartTime", (cinema_id,))
            else:
                cursor.execute(query + " ORDER BY c.CinemaName, s.StartTime")
            
            screenings = cursor.fetchall()
            
            # Insert data into treeview with actual cinema name
            for screening in screenings:
                cinema_name = screening["CinemaName"] if screening["CinemaName"] else "Not Assigned"
                self.screenings_tree.insert("", "end", values=(
                    screening["ScreeningID"],
                    cinema_name,
                    screening["Title"],
                    f"Screen {screening['ScreenNumber']}",
                    screening["StartTime"],
                    screening["EndTime"],
                    screening["TotalSeats"]
                ))
                
            if not screenings:
                self.screenings_tree.insert("", "end", values=("No screenings found", "", "", "", "", "", ""))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load screenings: {e}")
            self.screenings_tree.insert("", "end", values=("Error loading data", "", "", "", "", ""))
        finally:
            self.db.close()  # Use local db

    def show_add_screening_dialog(self):
        """Show dialog to add a new screening"""
        # Create a new window
        add_window = tk.Toplevel(self)
        add_window.title("Add New Screening")
        add_window.geometry("400x400")
        add_window.resizable(False, False)
        
        # Get films for dropdown
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT FilmID, Title FROM Films ORDER BY Title")
        films = cursor.fetchall()
        film_options = [f"{film['FilmID']} - {film['Title']}" for film in films]
        
        # Get screens for dropdown
        cursor.execute("SELECT ScreenID, ScreenNumber, SeatCapacity FROM Screens ORDER BY ScreenNumber")
        screens = cursor.fetchall()
        screen_options = [f"{screen['ScreenID']} - Screen {screen['ScreenNumber']} ({screen['SeatCapacity']} seats)" for screen in screens]
        self.db.close()
        
        # Film selection
        tk.Label(add_window, text="Select Film:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        film_combo = ttk.Combobox(add_window, width=30, values=film_options, state="readonly")
        if film_options:
            film_combo.current(0)
        film_combo.grid(row=0, column=1, padx=10, pady=5)
        
        # Screen selection
        tk.Label(add_window, text="Select Screen:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        screen_combo = ttk.Combobox(add_window, width=30, values=screen_options, state="readonly")
        if screen_options:
            screen_combo.current(0)
        screen_combo.grid(row=1, column=1, padx=10, pady=5)
        
        # Start time
        tk.Label(add_window, text="Start Time (HH:MM):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        start_entry = tk.Entry(add_window, width=30)
        start_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # End time
        tk.Label(add_window, text="End Time (HH:MM):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        end_entry = tk.Entry(add_window, width=30)
        end_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # VIP seats
        tk.Label(add_window, text="VIP Seats:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        vip_seats = tk.Entry(add_window, width=30)
        vip_seats.insert(0, "10")  # Default value
        vip_seats.grid(row=4, column=1, padx=10, pady=5)
        
        # Add button
        tk.Button(
            add_window, 
            text="Add Screening", 
            command=lambda: self.add_screening(
                film_combo.get().split(" - ")[0],
                screen_combo.get().split(" - ")[0],
                start_entry.get(),
                end_entry.get(),
                vip_seats.get(),
                add_window
            )
        ).grid(row=5, column=0, columnspan=2, pady=20)

    def add_screening(self, film_id, screen_id, start_time, end_time, vip_seats, window):
        """Add a new screening to the database"""
        try:
            # Validate inputs
            if not start_time or not end_time:
                messagebox.showerror("Error", "Please enter start and end times")
                return
                
            # Convert vip_seats to integer
            vip_seats = int(vip_seats)
            
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Get screen capacity
            cursor.execute("SELECT SeatCapacity FROM Screens WHERE ScreenID = ?", (screen_id,))
            screen = cursor.fetchone()
            if not screen:
                messagebox.showerror("Error", "Invalid screen selected")
                self.db.close()
                return
                
            total_seats = screen["SeatCapacity"]
            
            # Calculate seat distribution
            if vip_seats > total_seats * 0.2:  # Limit VIP seats to 20% of total
                messagebox.showerror("Error", f"Too many VIP seats. Maximum allowed: {int(total_seats * 0.2)}")
                self.db.close()
                return
                
            lower_seats = int((total_seats - vip_seats) * 0.4)  # 40% of remaining seats
            upper_seats = total_seats - vip_seats - lower_seats
            
            # Add the screening
            cursor.execute(
                """
                INSERT INTO Screenings (FilmID, ScreenID, StartTime, EndTime, TotalSeats, VIPSeats, LowerSeats, UpperSeats)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (film_id, screen_id, start_time, end_time, total_seats, vip_seats, lower_seats, upper_seats)
            )
            
            conn.commit()
            self.db.close()
            
            messagebox.showinfo("Success", "Screening added successfully!")
            window.destroy()
            self.load_screenings_data()  # Reload the screenings list
        except ValueError:
            messagebox.showerror("Error", "VIP seats must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add screening: {e}")

    def show_edit_screening_dialog(self):
        """Show dialog to edit selected screening"""
        selected = self.screenings_tree.selection()
        if not selected:
            messagebox.showinfo("Information", "Please select a screening to edit")
            return
            
        # Get selected screening data
        screening_id = self.screenings_tree.item(selected[0], "values")[0]
        
        # Get current screening data from database
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.*, f.Title as FilmTitle, scr.ScreenNumber
                FROM Screenings s
                JOIN Films f ON s.FilmID = f.FilmID
                JOIN Screens scr ON s.ScreenID = scr.ScreenID
                WHERE s.ScreeningID = ?
            """, (screening_id,))
            screening = cursor.fetchone()
            
            # Get films for dropdown
            cursor.execute("SELECT FilmID, Title FROM Films ORDER BY Title")
            films = cursor.fetchall()
            film_options = [f"{film['FilmID']} - {film['Title']}" for film in films]
            
            # Get screens for dropdown
            cursor.execute("SELECT ScreenID, ScreenNumber, SeatCapacity FROM Screens ORDER BY ScreenNumber")
            screens = cursor.fetchall()
            screen_options = [f"{screen['ScreenID']} - Screen {screen['ScreenNumber']} ({screen['SeatCapacity']} seats)" for screen in screens]
            self.db.close()
            
            if not screening:
                messagebox.showerror("Error", "Screening not found in database")
                return
                
            # Create edit dialog window
            edit_window = tk.Toplevel(self)
            edit_window.title(f"Edit Screening: {screening['FilmTitle']}")
            edit_window.geometry("400x400")
            edit_window.resizable(False, False)
            
            # Film selection
            tk.Label(edit_window, text="Select Film:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            film_combo = ttk.Combobox(edit_window, width=30, values=film_options, state="readonly")
            # Set the current film
            current_film_index = next((i for i, v in enumerate(film_options) if v.startswith(f"{screening['FilmID']} - ")), 0)
            film_combo.current(current_film_index)
            film_combo.grid(row=0, column=1, padx=10, pady=5)
            
            # Screen selection
            tk.Label(edit_window, text="Select Screen:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            screen_combo = ttk.Combobox(edit_window, width=30, values=screen_options, state="readonly")
            # Set the current screen
            current_screen_index = next((i for i, v in enumerate(screen_options) if v.startswith(f"{screening['ScreenID']} - ")), 0)
            screen_combo.current(current_screen_index)
            screen_combo.grid(row=1, column=1, padx=10, pady=5)
            
            # Start time
            tk.Label(edit_window, text="Start Time (HH:MM):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
            start_entry = tk.Entry(edit_window, width=30)
            start_entry.insert(0, screening['StartTime'])
            start_entry.grid(row=2, column=1, padx=10, pady=5)
            
            # End time
            tk.Label(edit_window, text="End Time (HH:MM):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
            end_entry = tk.Entry(edit_window, width=30)
            end_entry.insert(0, screening['EndTime'])
            end_entry.grid(row=3, column=1, padx=10, pady=5)
            
            # VIP seats
            tk.Label(edit_window, text="VIP Seats:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
            vip_seats = tk.Entry(edit_window, width=30)
            vip_seats.insert(0, screening['VIPSeats'])
            vip_seats.grid(row=4, column=1, padx=10, pady=5)
            
            # Update button
            tk.Button(
                edit_window, 
                text="Update Screening", 
                command=lambda: self.update_screening(
                    screening_id,
                    film_combo.get().split(" - ")[0],
                    screen_combo.get().split(" - ")[0],
                    start_entry.get(),
                    end_entry.get(),
                    vip_seats.get(),
                    edit_window
                )
            ).grid(row=5, column=0, columnspan=2, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load screening data: {e}")

    def update_screening(self, screening_id, film_id, screen_id, start_time, end_time, vip_seats, window):
        """Update an existing screening in the database"""
        try:
            # Validate inputs
            if not start_time or not end_time:
                messagebox.showerror("Error", "Please enter start and end times")
                return
                
            # Convert vip_seats to integer
            vip_seats = int(vip_seats)
            
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Check if screening has bookings
            cursor.execute("SELECT COUNT(*) FROM Bookings WHERE ScreeningID = ?", (screening_id,))
            booking_count = cursor.fetchone()[0]
            
            if booking_count > 0:
                if not messagebox.askyesno("Warning", f"This screening has {booking_count} bookings. Modifying it may affect existing bookings. Continue?"):
                    self.db.close()
                    return
            
            # Get screen capacity
            cursor.execute("SELECT SeatCapacity FROM Screens WHERE ScreenID = ?", (screen_id,))
            screen = cursor.fetchone()
            if not screen:
                messagebox.showerror("Error", "Invalid screen selected")
                self.db.close()
                return
                
            total_seats = screen["SeatCapacity"]
            
            # Calculate seat distribution
            if vip_seats > total_seats * 0.2:  # Limit VIP seats to 20% of total
                messagebox.showerror("Error", f"Too many VIP seats. Maximum allowed: {int(total_seats * 0.2)}")
                self.db.close()
                return
                
            lower_seats = int((total_seats - vip_seats) * 0.4)  # 40% of remaining seats
            upper_seats = total_seats - vip_seats - lower_seats
            
            # Update the screening
            cursor.execute(
                """
                UPDATE Screenings 
                SET FilmID = ?, ScreenID = ?, StartTime = ?, EndTime = ?, 
                    TotalSeats = ?, VIPSeats = ?, LowerSeats = ?, UpperSeats = ?
                WHERE ScreeningID = ?
                """,
                (film_id, screen_id, start_time, end_time, total_seats, vip_seats, lower_seats, upper_seats, screening_id)
            )
            
            conn.commit()
            self.db.close()
            
            messagebox.showinfo("Success", "Screening updated successfully!")
            window.destroy()
            self.load_screenings_data()  # Reload the screenings list
        except ValueError:
            messagebox.showerror("Error", "VIP seats must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update screening: {e}")

    def delete_screening(self):
        """Delete the selected screening"""
        selected = self.screenings_tree.selection()
        if not selected:
            messagebox.showinfo("Information", "Please select a screening to delete")
            return
            
        # Get selected screening data
        screening_id = self.screenings_tree.item(selected[0], "values")[0]
        film_title = self.screenings_tree.item(selected[0], "values")[1]
        start_time = self.screenings_tree.item(selected[0], "values")[3]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the screening of '{film_title}' at {start_time}?"):
            try:
                conn = self.db.connect()
                cursor = conn.cursor()
                
                # Check if screening has bookings
                cursor.execute("SELECT COUNT(*) FROM Bookings WHERE ScreeningID = ?", (screening_id,))
                booking_count = cursor.fetchone()[0]
                
                if booking_count > 0:
                    if not messagebox.askyesno("Warning", f"This screening has {booking_count} bookings. Deleting it will also delete all associated bookings. Continue?"):
                        self.db.close()
                        return
                
                # Delete the screening (cascade will handle bookings)
                cursor.execute("DELETE FROM Screenings WHERE ScreeningID = ?", (screening_id,))
                conn.commit()
                self.db.close()
                
                messagebox.showinfo("Success", "Screening deleted successfully!")
                self.load_screenings_data()  # Reload the screenings list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete screening: {e}")


    def setup_films_tab(self, parent):
        """Set up the films management tab"""
        # Films list frame
        list_frame = tk.Frame(parent)
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Films treeview
        columns = ("id", "title", "genre", "duration", "rating")
        self.films_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        self.films_tree.heading("id", text="ID")
        self.films_tree.heading("title", text="Title")
        self.films_tree.heading("genre", text="Genre")
        self.films_tree.heading("duration", text="Duration")
        self.films_tree.heading("rating", text="Rating")
        
        # Define column widths
        self.films_tree.column("id", width=50)
        self.films_tree.column("title", width=200)
        self.films_tree.column("genre", width=100)
        self.films_tree.column("duration", width=80)
        self.films_tree.column("rating", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.films_tree.yview)
        self.films_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        scrollbar.pack(side="right", fill="y")
        self.films_tree.pack(fill="both", expand=True)
        
        # Load films data
        self.load_films_data()
        
        # Films control frame
        control_frame = tk.Frame(parent)
        control_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        # Add film button
        add_button = tk.Button(
            control_frame,
            text="Add Film",
            width=15,
            command=self.show_add_film_dialog
        )
        add_button.pack(pady=5)
        
        # Edit film button
        edit_button = tk.Button(
            control_frame,
            text="Edit Film",
            width=15,
            command=self.show_edit_film_dialog
        )
        edit_button.pack(pady=5)
        
        # Delete film button
        delete_button = tk.Button(
            control_frame,
            text="Delete Film",
            width=15,
            command=self.delete_selected_film
        )
        delete_button.pack(pady=5)
        

    def load_films_data(self):
        """Load film data from database into treeview"""
        # Clear existing data
        for item in self.films_tree.get_children():
            self.films_tree.delete(item)
            
        # Get films data from database - use local db instance
        films = self.db.get_all_film_rows()
        
        # Insert into treeview
        for film in films:
            self.films_tree.insert("", "end", values=(
                film["FilmID"],
                film["Title"],
                film["Genre"],
                film["Duration"],
                film["Rating"]
            ))
    
    def show_add_film_dialog(self):
        """Show dialog to add a new film"""
        # Create a new window
        add_window = tk.Toplevel(self)
        add_window.title("Add New Film")
        add_window.geometry("400x400")
        add_window.resizable(False, False)
        
        # Title entry
        tk.Label(add_window, text="Title:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        title_entry = tk.Entry(add_window, width=30)
        title_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Description entry
        tk.Label(add_window, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        desc_entry = tk.Text(add_window, width=30, height=5)
        desc_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Actors entry
        tk.Label(add_window, text="Actors:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        actors_entry = tk.Entry(add_window, width=30)
        actors_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Genre entry
        tk.Label(add_window, text="Genre:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        genre_entry = tk.Entry(add_window, width=30)
        genre_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Rating entry
        tk.Label(add_window, text="Rating:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        rating_entry = tk.Entry(add_window, width=30)
        rating_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Duration entry
        tk.Label(add_window, text="Duration (mins):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        duration_entry = tk.Entry(add_window, width=30)
        duration_entry.grid(row=5, column=1, padx=10, pady=5)
        
        # Add button
        tk.Button(
            add_window, 
            text="Add Film", 
            command=lambda: self.add_film(
                title_entry.get(),
                desc_entry.get("1.0", "end-1c"),
                actors_entry.get(),
                genre_entry.get(),
                rating_entry.get(),
                duration_entry.get(),
                add_window
            )
        ).grid(row=6, column=0, columnspan=2, pady=20)
    
    def add_film(self, title, description, actors, genre, rating, duration, window):
        """Add a new film to the database"""
        try:
            duration = int(duration)
            film_id = self.db.add_film(title, description, actors, genre, rating, duration)
            if film_id:
                messagebox.showinfo("Success", f"Film '{title}' added successfully!")
                window.destroy()
                self.load_films_data()
                self.refresh_movie_list_page()
            else:
                messagebox.showerror("Error", "Failed to add film")
        except ValueError:
            messagebox.showerror("Error", "Duration must be a number")
    
    def show_edit_film_dialog(self):
        """Show dialog to edit selected film"""
        selected = self.films_tree.selection()
        if not selected:
            messagebox.showinfo("Information", "Please select a film to edit")
            return
            
        # Get selected film data
        film_id = self.films_tree.item(selected[0], "values")[0]
        
        # Get current film data from database
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Films WHERE FilmID = ?", (film_id,))
            film = cursor.fetchone()
            self.db.close()
            
            if not film:
                messagebox.showerror("Error", "Film not found in database")
                return
                
            # Create edit dialog window
            edit_window = tk.Toplevel(self)
            edit_window.title(f"Edit Film: {film['Title']}")
            edit_window.geometry("400x400")
            edit_window.resizable(False, False)
            
            # Title entry
            tk.Label(edit_window, text="Title:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            title_entry = tk.Entry(edit_window, width=30)
            title_entry.insert(0, film['Title'])
            title_entry.grid(row=0, column=1, padx=10, pady=5)
            
            # Description entry
            tk.Label(edit_window, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            desc_entry = tk.Text(edit_window, width=30, height=5)
            desc_entry.insert("1.0", film['Description'] if film['Description'] else "")
            desc_entry.grid(row=1, column=1, padx=10, pady=5)
            
            # Actors entry
            tk.Label(edit_window, text="Actors:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
            actors_entry = tk.Entry(edit_window, width=30)
            actors_entry.insert(0, film['Actors'] if film['Actors'] else "")
            actors_entry.grid(row=2, column=1, padx=10, pady=5)
            
            # Genre entry
            tk.Label(edit_window, text="Genre:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
            genre_entry = tk.Entry(edit_window, width=30)
            genre_entry.insert(0, film['Genre'] if film['Genre'] else "")
            genre_entry.grid(row=3, column=1, padx=10, pady=5)
            
            # Rating entry
            tk.Label(edit_window, text="Rating:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
            rating_entry = tk.Entry(edit_window, width=30)
            rating_entry.insert(0, film['Rating'] if film['Rating'] else "")
            rating_entry.grid(row=4, column=1, padx=10, pady=5)
            
            # Duration entry
            tk.Label(edit_window, text="Duration (mins):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
            duration_entry = tk.Entry(edit_window, width=30)
            duration_entry.insert(0, film['Duration'])
            duration_entry.grid(row=5, column=1, padx=10, pady=5)
            
            # Update button
            tk.Button(
                edit_window, 
                text="Update Film", 
                command=lambda: self.update_film(
                    film_id,
                    title_entry.get(),
                    desc_entry.get("1.0", "end-1c"),
                    actors_entry.get(),
                    genre_entry.get(),
                    rating_entry.get(),
                    duration_entry.get(),
                    edit_window
                )
            ).grid(row=6, column=0, columnspan=2, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load film data: {e}")

    def update_film(self, film_id, title, description, actors, genre, rating, duration, window):
        """Update an existing film in the database"""
        try:
            duration = int(duration)
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Films 
                SET Title = ?, Description = ?, Actors = ?, Genre = ?, Rating = ?, Duration = ?
                WHERE FilmID = ?
                """,
                (title, description, actors, genre, rating, duration, film_id)
            )
            conn.commit()
            self.db.close()
            
            messagebox.showinfo("Success", f"Film '{title}' updated successfully!")
            window.destroy()
            self.load_films_data()
            self.refresh_movie_list_page()
        except ValueError:
            messagebox.showerror("Error", "Duration must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update film: {e}")

    def delete_selected_film(self):
        """Delete the selected film"""
        selected = self.films_tree.selection()
        if not selected:
            messagebox.showinfo("Information", "Please select a film to delete")
            return
            
        # Get selected film data
        film_id = self.films_tree.item(selected[0], "values")[0]
        film_title = self.films_tree.item(selected[0], "values")[1]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{film_title}'?"):
            try:
                conn = self.db.connect()
                cursor = conn.cursor()
                
                # Check if film has any screenings
                cursor.execute("SELECT COUNT(*) FROM Screenings WHERE FilmID = ?", (film_id,))
                screening_count = cursor.fetchone()[0]
                
                if screening_count > 0:
                    if not messagebox.askyesno("Warning", f"This film has {screening_count} screenings scheduled. Deleting it will also delete all associated screenings and bookings. Continue?"):
                        self.db.close()
                        return
                
                # Delete the film (cascade will handle related screenings and bookings)
                cursor.execute("DELETE FROM Films WHERE FilmID = ?", (film_id,))
                conn.commit()
                self.db.close()
                
                messagebox.showinfo("Success", f"Film '{film_title}' deleted successfully!")
                self.load_films_data()
                self.refresh_movie_list_page()  
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete film: {e}")



    def refresh_movie_list_page(self):
        """Refresh the MovieListPage if it exists in the controller's frames"""
        for frame_name, frame in self.controller.frames.items():
            if frame_name == "MovieListPage":
                new_page = frame.__class__(self.controller.container, self.controller)
                self.controller.frames[frame_name] = new_page
                new_page.grid(row=0, column=0, sticky="nsew")
                break



    def setup_reports_tab(self, parent):
        """Set up the reports tab"""
        # Reports frame
        list_frame = tk.Frame(parent)
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Report types frame
        report_types_frame = tk.LabelFrame(list_frame, text="Report Types")
        report_types_frame.pack(fill="x", pady=10)
        
        # Report type buttons
        tk.Button(
            report_types_frame,
            text="Booking Revenue",
            width=20,
            command=lambda: self.show_revenue_report()
        ).pack(side="left", padx=10, pady=10)
        
        tk.Button(
            report_types_frame,
            text="Popular Films",
            width=20,
            command=lambda: self.show_popular_films_report()
        ).pack(side="left", padx=10, pady=10)
        
        tk.Button(
            report_types_frame,
            text="Cinema Performance",
            width=20,
            command=lambda: self.show_cinema_report()
        ).pack(side="left", padx=10, pady=10)
        
        # Add refresh button for reports
        refresh_button = tk.Button(
            report_types_frame,
            text="Refresh Report",
            width=20,
            command=self.refresh_current_report
        )
        refresh_button.pack(side="left", padx=10, pady=10)
        
        # Add export button for reports
        export_button = tk.Button(
            report_types_frame,
            text="Export Report",
            width=20,
            command=self.export_current_report,
            bg="#4CAF50",
            fg="white"
        )
        export_button.pack(side="left", padx=10, pady=10)
        
        # Report results frame
        report_frame = tk.LabelFrame(list_frame, text="Report Results")
        report_frame.pack(fill="both", expand=True, pady=10)
        
        # Results treeview
        columns = ("item", "value1", "value2", "value3")
        self.report_tree = ttk.Treeview(report_frame, columns=columns, show="headings")
        
        # Define headings (these will change based on report type)
        self.report_tree.heading("item", text="Item")
        self.report_tree.heading("value1", text="Value 1")
        self.report_tree.heading("value2", text="Value 2")
        self.report_tree.heading("value3", text="Value 3")
        
        # Define column widths
        self.report_tree.column("item", width=200)
        self.report_tree.column("value1", width=100)
        self.report_tree.column("value2", width=100)
        self.report_tree.column("value3", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(report_frame, orient="vertical", command=self.report_tree.yview)
        self.report_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        scrollbar.pack(side="right", fill="y")
        self.report_tree.pack(fill="both", expand=True)
        
        # Store the current report type
        self.current_report = None
        
        # Add a frame for visualizations
        self.viz_frame = tk.LabelFrame(list_frame, text="Visualization")
        self.viz_frame.pack(fill="both", expand=True, pady=10)

    def refresh_current_report(self):
        """Refresh the currently displayed report"""
        if self.current_report == "revenue":
            self.show_revenue_report()
        elif self.current_report == "films":
            self.show_popular_films_report()
        elif self.current_report == "cinema":
            self.show_cinema_report()
        else:
            messagebox.showinfo("Information", "Please select a report type first")

    def show_revenue_report(self):
        """Display the revenue report from actual bookings data"""
        self.current_report = "revenue"
        # Clear existing data
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # Update column headers
        self.report_tree.heading("item", text="Cinema")
        self.report_tree.heading("value1", text="Revenue (£)")
        self.report_tree.heading("value2", text="Bookings")
        self.report_tree.heading("value3", text="Avg. Price (£)")
        
        try:
            # Connect to database - use local db instance
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Query to get booking revenue by cinema
            cursor.execute("""
                SELECT 
                    c.CinemaName as Cinema,
                    SUM(b.TotalPrice) as Revenue,
                    COUNT(b.BookingID) as BookingCount,
                    ROUND(AVG(b.TotalPrice), 2) as AvgPrice
                FROM Bookings b
                JOIN Cinemas c ON b.CinemaID = c.CinemaID
                WHERE b.Status = 'active'
                GROUP BY c.CinemaID
                ORDER BY Revenue DESC
            """)
            
            results = cursor.fetchall()
            
            # Insert data into treeview
            for row in results:
                self.report_tree.insert("", "end", values=(
                    row["Cinema"],
                    f"{row['Revenue']:.2f}",
                    row["BookingCount"],
                    f"{row['AvgPrice']:.2f}"
                ))
                
            if not results:
                self.report_tree.insert("", "end", values=("No revenue data found", "", "", ""))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load revenue report: {e}")
            self.report_tree.insert("", "end", values=("Error loading data", "", "", ""))
        finally:
            self.db.close()
            
        self.display_visualization_in_app()

    def show_popular_films_report(self):
        """Display report of most popular films based on booking data"""
        self.current_report = "films"
        # Clear existing data
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # Update column headers
        self.report_tree.heading("item", text="Film Title")
        self.report_tree.heading("value1", text="Bookings")
        self.report_tree.heading("value2", text="Revenue (£)")
        self.report_tree.heading("value3", text="Avg. Seats/Booking")
        
        try:
            # Connect to database
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Query to get popular films data
            cursor.execute("""
                SELECT 
                    f.Title as FilmTitle,
                    COUNT(DISTINCT b.BookingID) as BookingCount,
                    SUM(b.TotalPrice) as Revenue,
                    ROUND(COUNT(bs.BookingSeatID) * 1.0 / COUNT(DISTINCT b.BookingID), 1) as AvgSeatsPerBooking
                FROM Films f
                JOIN Screenings s ON f.FilmID = s.FilmID
                JOIN Bookings b ON s.ScreeningID = b.ScreeningID
                LEFT JOIN BookingSeats bs ON b.BookingID = bs.BookingID
                WHERE b.Status = 'active'
                GROUP BY f.FilmID
                ORDER BY BookingCount DESC
            """)
            
            results = cursor.fetchall()
            
            # Insert data into treeview
            for row in results:
                self.report_tree.insert("", "end", values=(
                    row["FilmTitle"],
                    row["BookingCount"],
                    f"{row['Revenue']:.2f}" if row['Revenue'] else "0.00",
                    row["AvgSeatsPerBooking"]
                ))
                
            if not results:
                self.report_tree.insert("", "end", values=("No film booking data found", "", "", ""))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load popular films report: {e}")
            self.report_tree.insert("", "end", values=("Error loading data", "", "", ""))
        finally:
            self.db.close()

        self.display_visualization_in_app()

    def show_cinema_report(self):
        """Display performance report for each cinema"""
        self.current_report = "cinema"
        # Clear existing data
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # Update column headers
        self.report_tree.heading("item", text="Cinema")
        self.report_tree.heading("value1", text="Occupancy Rate")
        self.report_tree.heading("value2", text="Avg. Revenue/Screening")
        self.report_tree.heading("value3", text="Popular Time Slot")
        
        try:
            # Connect to database
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Query to get cinema performance data
            cursor.execute("""
                SELECT 
                    c.CinemaName as CinemaName,
                    ROUND((COUNT(bs.BookingSeatID) * 100.0) / 
                        (SELECT SUM(scr.SeatCapacity) FROM Screenings s2 
                         JOIN Screens scr ON s2.ScreenID = scr.ScreenID
                         WHERE s2.ScreeningID IN (SELECT ScreeningID FROM Bookings WHERE CinemaID = c.CinemaID)), 1) 
                        as OccupancyRate,
                    ROUND(SUM(b.TotalPrice) / COUNT(DISTINCT s.ScreeningID), 2) as AvgRevenuePerScreening,
                    CASE 
                        WHEN CAST(substr(s.StartTime, 1, 2) as INTEGER) < 12 THEN 'Morning'
                        WHEN CAST(substr(s.StartTime, 1, 2) as INTEGER) < 17 THEN 'Afternoon'
                        ELSE 'Evening'
                    END as PopularTimeSlot
                FROM Cinemas c
                JOIN Bookings b ON c.CinemaID = b.CinemaID
                JOIN Screenings s ON b.ScreeningID = s.ScreeningID
                LEFT JOIN BookingSeats bs ON b.BookingID = bs.BookingID
                WHERE b.Status = 'active'
                GROUP BY c.CinemaID
                ORDER BY OccupancyRate DESC
            """)
            
            results = cursor.fetchall()
            
            # Insert data into treeview
            for row in results:
                self.report_tree.insert("", "end", values=(
                    row["CinemaName"],
                    f"{row['OccupancyRate']}%" if row['OccupancyRate'] else "N/A",
                    f"£{row['AvgRevenuePerScreening']:.2f}" if row['AvgRevenuePerScreening'] else "£0.00",
                    row["PopularTimeSlot"]
                ))
                
            if not results:
                self.report_tree.insert("", "end", values=("No cinema performance data found", "", "", ""))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load cinema report: {e}")
            self.report_tree.insert("", "end", values=("Error loading data", "", "", ""))
        finally:
            self.db.close()

        self.display_visualization_in_app()

    def export_current_report(self):
        """Export the current report to CSV and generate visualization"""
        if not self.current_report:
            messagebox.showinfo("Export Report", "Please select a report type first")
            return
        
        # Ask user for directory to save files
        export_dir = filedialog.askdirectory(title="Select Export Directory")
        if not export_dir:
            return  # User canceled
        
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"{self.current_report}_report_{timestamp}"
            
            # Get report data from treeview
            report_data = []
            headers = [self.report_tree.heading(col)["text"] for col in self.report_tree["columns"]]
            report_data.append(headers)
            
            for item_id in self.report_tree.get_children():
                item_values = self.report_tree.item(item_id, "values")
                report_data.append(item_values)
            
            # Export to CSV
            csv_path = os.path.join(export_dir, f"{report_name}.csv")
            with open(csv_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                for row in report_data:
                    csv_writer.writerow(row)
            
            # Generate and save visualization
            self.generate_report_visualization(export_dir, report_name)
            
            messagebox.showinfo("Export Complete", 
                               f"Report exported successfully to:\n{export_dir}\n\n"
                               f"Files created:\n"
                               f"- {report_name}.csv (Data)\n"
                               f"- {report_name}.png (Chart)")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export report: {str(e)}")

    def generate_report_visualization(self, export_dir, report_name):
        """Generate visualization based on the current report type"""
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Get data from treeview
        items = []
        values = []
        
        for item_id in self.report_tree.get_children():
            item_values = self.report_tree.item(item_id, "values")
            if len(item_values) >= 2 and item_values[0] != "No data" and not item_values[0].startswith("Error"):
                items.append(item_values[0])
                # Try to convert value to float, removing currency symbols if needed
                try:
                    val = item_values[1].replace('£', '').replace('%', '')
                    values.append(float(val))
                except (ValueError, TypeError):
                    values.append(0)
        
        if not items:  # No data to visualize
            # Create a simple message chart
            ax.text(0.5, 0.5, "No data to visualize", 
                    horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            ax.axis('off')
        else:
            # Create chart based on report type
            if self.current_report == "revenue":
                # Bar chart for revenue
                bars = ax.bar(items, values, color='skyblue')
                ax.set_title('Revenue by Cinema')
                ax.set_xlabel('Cinema')
                ax.set_ylabel('Revenue (£)')
                ax.set_xticklabels(items, rotation=45, ha='right')
                ax.grid(axis='y', linestyle='--', alpha=0.7)
                
                # Add value labels on top of bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                            f'£{height:.2f}', ha='center', va='bottom')
                    
            elif self.current_report == "films":
                # Horizontal bar chart for popular films
                bars = ax.barh(items, values, color='lightgreen')
                ax.set_title('Most Popular Films by Bookings')
                ax.set_xlabel('Number of Bookings')
                ax.set_ylabel('Film Title')
                ax.grid(axis='x', linestyle='--', alpha=0.7)
                
                # Add value labels at end of bars
                for bar in bars:
                    width = bar.get_width()
                    ax.text(width + 0.3, bar.get_y() + bar.get_height()/2.,
                            f'{width:.0f}', ha='left', va='center')
                    
            elif self.current_report == "cinema":
                # Pie chart for occupancy rates
                # Clean values: remove % and convert to float
                clean_values = []
                for val in values:
                    if isinstance(val, str) and '%' in val:
                        clean_values.append(float(val.replace('%', '')))
                    else:
                        clean_values.append(float(val) if val else 0)
                        
                ax.pie(clean_values, labels=items, autopct='%1.1f%%', 
                       startangle=90, shadow=True, explode=[0.05]*len(items))
                ax.set_title('Cinema Occupancy Rates')
                ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
        
        plt.tight_layout()
        
        # Save the figure
        chart_path = os.path.join(export_dir, f"{report_name}.png")
        fig.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        # Additionally, display the visualization in the application
        self.display_visualization_in_app(fig)

    def display_visualization_in_app(self, fig=None):
        """Display the current visualization in the application"""
        # Clear the visualization frame
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
            
        if not fig:
            # If no figure is provided, generate one based on current report
            if not self.current_report:
                return
                
            fig, ax = plt.subplots(figsize=(8, 4))
            
            # Get data from treeview (similar to above)
            items = []
            values = []
            
            for item_id in self.report_tree.get_children():
                item_values = self.report_tree.item(item_id, "values")
                if len(item_values) >= 2 and item_values[0] != "No data" and not item_values[0].startswith("Error"):
                    items.append(item_values[0])
                    try:
                        val = item_values[1].replace('£', '').replace('%', '')
                        values.append(float(val))
                    except (ValueError, TypeError):
                        values.append(0)
                        
            if not items:
                return
                
            # Generate visualization based on current report type
            # (similar logic to generate_report_visualization)
            if self.current_report == "revenue":
                ax.bar(items, values, color='skyblue')
                ax.set_title('Revenue by Cinema')
            elif self.current_report == "films":
                ax.barh(items, values, color='lightgreen')
                ax.set_title('Most Popular Films')
            elif self.current_report == "cinema":
                ax.bar(items, values, color='salmon')
                ax.set_title('Cinema Performance')
                
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
        
        # Create a canvas to display the figure in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()