"""
Admin page functions
"""
import tkinter as tk
from tkinter import ttk, messagebox
from Basepage import BasePage
from Database import Database  # Make sure this import is present

#Harry Elson, 23021935
#Matt Nogodula, 23015215
#Jerry Lin, 23024553

class AdminPage(BasePage):
    """Admin page for system management"""
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
            text="Admin Dashboard",
            font=("Arial", 16, "bold"),
            bg="white"
        )
        page_title.pack(anchor="w", pady=(0, 20))
        
        # Tabs for different admin functions
        tab_control = ttk.Notebook(content)
        
        # Films tab
        films_tab = ttk.Frame(tab_control)
        tab_control.add(films_tab, text="Films Management")
        
        # Screenings tab
        screenings_tab = ttk.Frame(tab_control)
        tab_control.add(screenings_tab, text="Screenings")
        
        # Users tab
        users_tab = ttk.Frame(tab_control)
        tab_control.add(users_tab, text="Users")

        staff_tab = ttk.Frame(tab_control)
        tab_control.add(staff_tab, text="Staff")

        # Reports tab
        reports_tab = ttk.Frame(tab_control)
        tab_control.add(reports_tab, text="Reports")
        
        tab_control.pack(expand=1, fill="both")
        
        # Set up tabs with data
        self.setup_films_tab(films_tab)
        self.setup_screenings_tab(screenings_tab)
        self.setup_reports_tab(reports_tab)
        self.setup_users_tab(users_tab)
        self.setup_staff_tab(staff_tab)
    
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
        
        # Add refresh button
        refresh_button = tk.Button(
            control_frame,
            text="Refresh List",
            width=15,
            command=self.load_films_data
        )
        refresh_button.pack(pady=5)

    def load_films_data(self):
        """Load film data from database into treeview"""
        # Clear existing data
        for item in self.films_tree.get_children():
            self.films_tree.delete(item)
            
        # Get films data from database - use local db instance
        films = self.db.get_all_film_rows()
        
        # Insert into treeview
        for film in films:
            self.films_tree.insert("", "end", values=(film["FilmID"], film["Title"], film["Genre"], film["Duration"], film["Rating"]))
    
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
                self.load_films_data()  # Reload the films list
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
            self.load_films_data()  # Reload the films list
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
                self.load_films_data()  # Reload the films list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete film: {e}")

    def setup_screenings_tab(self, parent):
        """Set up the screenings management tab"""
        # Screenings list frame
        list_frame = tk.Frame(parent)
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Screenings treeview
        columns = ("id", "film", "screen", "start_time", "end_time", "seats")
        self.screenings_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        self.screenings_tree.heading("id", text="ID")
        self.screenings_tree.heading("film", text="Film")
        self.screenings_tree.heading("screen", text="Screen")
        self.screenings_tree.heading("start_time", text="Start Time")
        self.screenings_tree.heading("end_time", text="End Time")
        self.screenings_tree.heading("seats", text="Total Seats")
        
        # Define column widths
        self.screenings_tree.column("id", width=50)
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
        
        # Load screenings data
        self.load_screenings_data()
        
        # Control frame
        control_frame = tk.Frame(parent)
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
            command=self.load_screenings_data
        )
        refresh_button.pack(pady=5)

    def load_screenings_data(self):
        """Load screenings data from database into treeview"""
        # Clear existing data
        for item in self.screenings_tree.get_children():
            self.screenings_tree.delete(item)
            
        try:
            # Connect to database - use local db instance
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Join query to get film name and screen info with screening details
            cursor.execute("""
                SELECT s.ScreeningID, f.Title, scr.ScreenNumber, s.StartTime, s.EndTime, s.TotalSeats
                FROM Screenings s
                JOIN Films f ON s.FilmID = f.FilmID
                JOIN Screens scr ON s.ScreenID = scr.ScreenID
                ORDER BY s.StartTime
            """)
            
            screenings = cursor.fetchall()
            
            # Insert data into treeview
            for screening in screenings:
                self.screenings_tree.insert("", "end", values=(
                    screening["ScreeningID"],
                    screening["Title"],
                    f"Screen {screening['ScreenNumber']}",
                    screening["StartTime"],
                    screening["EndTime"],
                    screening["TotalSeats"]
                ))
                
            if not screenings:
                self.screenings_tree.insert("", "end", values=("No screenings found", "", "", "", "", ""))
                
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
            self.db.close()  # Use local db
    
    def show_popular_films_report(self):
        """Display the popular films report from actual data"""
        self.current_report = "films"
        # Clear existing data
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # Update column headers
        self.report_tree.heading("item", text="Film")
        self.report_tree.heading("value1", text="Tickets Sold")
        self.report_tree.heading("value2", text="Revenue (£)")
        self.report_tree.heading("value3", text="Screenings")
        
        try:
            # Connect to database - use local db instance
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Query to get popular films data
            cursor.execute("""
                SELECT 
                    f.Title as Film,
                    COUNT(bs.BookingSeatID) as TicketsSold,
                    SUM(b.TotalPrice) as Revenue,
                    (SELECT COUNT(*) FROM Screenings WHERE FilmID = f.FilmID) as ScreeningCount
                FROM Films f
                JOIN Screenings scr ON f.FilmID = scr.FilmID
                JOIN Bookings b ON scr.ScreeningID = b.ScreeningID
                JOIN BookingSeats bs ON b.BookingID = bs.BookingID
                WHERE b.Status = 'active'
                GROUP BY f.FilmID
                ORDER BY TicketsSold DESC
            """)
            
            results = cursor.fetchall()
            
            # Insert data into treeview
            for row in results:
                self.report_tree.insert("", "end", values=(
                    row["Film"],
                    row["TicketsSold"],
                    f"{row['Revenue']:.2f}",
                    row["ScreeningCount"]
                ))
                
            if not results:
                self.report_tree.insert("", "end", values=("No film performance data found", "", "", ""))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load films report: {e}")
            self.report_tree.insert("", "end", values=("Error loading data", "", "", ""))
        finally:
            self.db.close()  # Use local db
    
    def show_cinema_report(self):
        """Display the cinema performance report from actual data"""
        self.current_report = "cinema"
        # Clear existing data
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # Update column headers
        self.report_tree.heading("item", text="Cinema")
        self.report_tree.heading("value1", text="Occupancy %")
        self.report_tree.heading("value2", text="Screenings")
        self.report_tree.heading("value3", text="Active Bookings")
        
        try:
            # Connect to database - use local db instance
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Query to get cinema performance data
            cursor.execute("""
                SELECT 
                    c.CinemaName as Cinema,
                    (COUNT(bs.BookingSeatID) * 100.0 / 
                        (SELECT SUM(sc.TotalSeats) 
                         FROM Screenings sc
                         JOIN Bookings b ON sc.ScreeningID = b.ScreeningID
                         WHERE b.CinemaID = c.CinemaID)) as Occupancy,
                    COUNT(DISTINCT scr.ScreeningID) as ScreeningCount,
                    COUNT(DISTINCT b.BookingID) as BookingCount
                FROM Cinemas c
                JOIN Bookings b ON c.CinemaID = b.CinemaID
                JOIN Screenings scr ON b.ScreeningID = scr.ScreeningID
                LEFT JOIN BookingSeats bs ON b.BookingID = bs.BookingID
                WHERE b.Status = 'active'
                GROUP BY c.CinemaID
                ORDER BY Occupancy DESC
            """)
            
            results = cursor.fetchall()
            
            # Insert data into treeview
            for row in results:
                self.report_tree.insert("", "end", values=(
                    row["Cinema"],
                    f"{row['Occupancy']:.1f}%",
                    row["ScreeningCount"],
                    row["BookingCount"]
                ))
                
            if not results:
                self.report_tree.insert("", "end", values=("No cinema performance data found", "", "", ""))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load cinema report: {e}")
            self.report_tree.insert("", "end", values=("Error loading data", "", "", ""))
        finally:
            self.db.close()  # Use local db
    
    def setup_users_tab(self, parent):
        """Set up the users management tab"""
        # Users list frame
        list_frame = tk.Frame(parent)
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Users treeview
        columns = ("id", "username", "email", "role")
        self.users_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        self.users_tree.heading("id", text="ID")
        self.users_tree.heading("username", text="Username")
        self.users_tree.heading("email", text="Email")
        self.users_tree.heading("role", text="Role")
        
        # Define column widths
        self.users_tree.column("id", width=50)
        self.users_tree.column("username", width=150)
        self.users_tree.column("email", width=200)
        self.users_tree.column("role", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        scrollbar.pack(side="right", fill="y")
        self.users_tree.pack(fill="both", expand=True)
        
        # Load users data
        self.load_users_data()
        
        # Control frame
        control_frame = tk.Frame(parent)
        control_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        # Add user button
        add_button = tk.Button(
            control_frame,
            text="Add User",
            width=15,
            command=self.show_add_user_dialog
        )
        add_button.pack(pady=5)
        
        # Edit user button
        edit_button = tk.Button(
            control_frame,
            text="Edit User",
            width=15,
            command=self.show_edit_user_dialog
        )
        edit_button.pack(pady=5)
        
        # Delete user button
        delete_button = tk.Button(
            control_frame,
            text="Delete User",
            width=15,
            command=self.delete_user
        )
        delete_button.pack(pady=5)
        
        # Add refresh button
        refresh_button = tk.Button(
            control_frame,
            text="Refresh List",
            width=15,
            command=self.load_users_data
        )
        refresh_button.pack(pady=5)
    
    def load_users_data(self):
        """Load users data from database into treeview"""
        # Clear existing data
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        try:
            # Connect to database - use local db instance
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Query to get users data
            cursor.execute("""
                SELECT 
                    u.UserID, 
                    u.Username, 
                    u.Email, 
                    r.RoleName
                FROM Users u
                JOIN Roles r ON u.RoleID = r.RoleID
                ORDER BY u.UserID
            """)
            
            users = cursor.fetchall()
            
            # Insert data into treeview
            for user in users:
                self.users_tree.insert("", "end", values=(
                    user["UserID"],
                    user["Username"],
                    user["Email"],
                    user["RoleName"]
                ))
                
            if not users:
                self.users_tree.insert("", "end", values=("No users found", "", "", ""))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load users: {e}")
            self.users_tree.insert("", "end", values=("Error loading data", "", "", ""))
        finally:
            self.db.close()  # Use local db
    
    def show_add_user_dialog(self):
        """Show dialog to add a new user"""
        # Create a new window
        add_window = tk.Toplevel(self)
        add_window.title("Add New User")
        add_window.geometry("400x350")
        add_window.resizable(False, False)
        
        # Get roles for dropdown
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT RoleID, RoleName FROM Roles ORDER BY RoleName")
        roles = cursor.fetchall()
        role_options = [f"{role['RoleName']}" for role in roles]
        self.db.close()
        
        # Username entry
        tk.Label(add_window, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        username_entry = tk.Entry(add_window, width=30)
        username_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Password entry
        tk.Label(add_window, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        password_entry = tk.Entry(add_window, width=30, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Confirm password entry
        tk.Label(add_window, text="Confirm Password:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        confirm_entry = tk.Entry(add_window, width=30, show="*")
        confirm_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Email entry
        tk.Label(add_window, text="Email:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        email_entry = tk.Entry(add_window, width=30)
        email_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Role selection
        tk.Label(add_window, text="Role:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        role_combo = ttk.Combobox(add_window, width=28, values=role_options, state="readonly")
        role_combo.current(2)  # Default to Customer
        role_combo.grid(row=4, column=1, padx=10, pady=5)
        
        # Add button
        tk.Button(
            add_window, 
            text="Add User", 
            command=lambda: self.add_user(
                username_entry.get(),
                password_entry.get(),
                confirm_entry.get(),
                email_entry.get(),
                role_combo.get(),
                add_window
            )
        ).grid(row=5, column=0, columnspan=2, pady=20)
    
    def add_user(self, username, password, confirm_password, email, role, window):
        """Add a new user to the database"""
        # Validate inputs
        if not username or not password or not email:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        # Email validation (simple check)
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        try:
            # Add the user
            success, message = self.db.create_user(username, password, email, role)
            
            if success:
                messagebox.showinfo("Success", f"User '{username}' added successfully!")
                window.destroy()
                self.load_users_data()  # Reload the users list
            else:
                messagebox.showerror("Error", message)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add user: {e}")
            
    def show_edit_user_dialog(self):
        """Show dialog to edit selected user"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showinfo("Information", "Please select a user to edit")
            return
            
        # Get selected user data
        user_id = self.users_tree.item(selected[0], "values")[0]
        
        # Get current user data from database
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.*, r.RoleName 
                FROM Users u
                JOIN Roles r ON u.RoleID = r.RoleID
                WHERE u.UserID = ?
            """, (user_id,))
            user = cursor.fetchone()
            
            # Get roles for dropdown
            cursor.execute("SELECT RoleID, RoleName FROM Roles ORDER BY RoleName")
            roles = cursor.fetchall()
            role_options = [f"{role['RoleName']}" for role in roles]
            self.db.close()
            
            if not user:
                messagebox.showerror("Error", "User not found in database")
                return
                
            # Create edit dialog window
            edit_window = tk.Toplevel(self)
            edit_window.title(f"Edit User: {user['Username']}")
            edit_window.geometry("400x300")
            edit_window.resizable(False, False)
            
            # Username (display only)
            tk.Label(edit_window, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            username_label = tk.Label(edit_window, text=user['Username'])
            username_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
            
            # Email entry
            tk.Label(edit_window, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            email_entry = tk.Entry(edit_window, width=30)
            email_entry.insert(0, user['Email'])
            email_entry.grid(row=1, column=1, padx=10, pady=5)
            
            # Role selection
            tk.Label(edit_window, text="Role:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
            role_combo = ttk.Combobox(edit_window, width=28, values=role_options, state="readonly")
            # Set the current role
            current_role_index = next((i for i, v in enumerate(role_options) if v == user['RoleName']), 0)
            role_combo.current(current_role_index)
            role_combo.grid(row=2, column=1, padx=10, pady=5)
            
            # Reset password checkbox
            reset_var = tk.BooleanVar()
            reset_check = tk.Checkbutton(edit_window, text="Reset password", variable=reset_var)
            reset_check.grid(row=3, column=0, columnspan=2, pady=5)
            
            # New password entry (initially hidden)
            password_frame = tk.Frame(edit_window)
            password_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")
            password_frame.grid_remove()  # Initially hidden
            
            tk.Label(password_frame, text="New Password:").grid(row=0, column=0, padx=10, sticky="w")
            new_password_entry = tk.Entry(password_frame, width=20, show="*")
            new_password_entry.grid(row=0, column=1, padx=10)
            
            # Show/hide password fields based on checkbox
            def toggle_password_fields():
                if reset_var.get():
                    password_frame.grid()
                else:
                    password_frame.grid_remove()
                    
            reset_check.config(command=toggle_password_fields)
            
            # Update button
            tk.Button(
                edit_window, 
                text="Update User", 
                command=lambda: self.update_user(
                    user_id,
                    email_entry.get(),
                    role_combo.get(),
                    reset_var.get(),
                    new_password_entry.get() if reset_var.get() else None,
                    edit_window
                )
            ).grid(row=5, column=0, columnspan=2, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load user data: {e}")

    def update_user(self, user_id, email, role, reset_password, new_password, window):
        """Update an existing user in the database"""
        # Validate inputs
        if not email:
            messagebox.showerror("Error", "Email cannot be empty")
            return
            
        # Email validation (simple check)
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address")
            return
            
        if reset_password and (not new_password or len(new_password) < 6):
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Get role ID
            cursor.execute("SELECT RoleID FROM Roles WHERE RoleName = ?", (role,))
            role_id = cursor.fetchone()["RoleID"]
            
            # Update user info
            cursor.execute(
                "UPDATE Users SET Email = ?, RoleID = ? WHERE UserID = ?",
                (email, role_id, user_id)
            )
            
            # Update password if requested
            if reset_password:
                import hashlib
                password_hash = hashlib.sha256(new_password.encode()).hexdigest()
                cursor.execute(
                    "UPDATE Users SET PasswordHash = ? WHERE UserID = ?",
                    (password_hash, user_id)
                )
            
            conn.commit()
            self.db.close()
            
            messagebox.showinfo("Success", "User updated successfully!")
            window.destroy()
            self.load_users_data()  # Reload the users list
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {e}")

    def delete_user(self):
        """Delete the selected user"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showinfo("Information", "Please select a user to delete")
            return
            
        # Get selected user data
        user_id = self.users_tree.item(selected[0], "values")[0]
        username = self.users_tree.item(selected[0], "values")[1]
        role = self.users_tree.item(selected[0], "values")[3]
        
        # Prevent deleting the admin user
        if username.lower() == "admin":
            messagebox.showerror("Error", "Cannot delete the admin user")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{username}'?"):
            try:
                conn = self.db.connect()
                cursor = conn.cursor()
                
                # Check if user is a customer with bookings
                if role == "Customer":
                    cursor.execute("""
                        SELECT COUNT(*) FROM Customers c 
                        JOIN Users u ON c.Email = u.Email
                        JOIN Bookings b ON b.CustomerID = c.CustomerID
                        WHERE u.UserID = ?
                    """, (user_id,))
                    booking_count = cursor.fetchone()[0]
                    
                    if booking_count > 0:
                        if not messagebox.askyesno("Warning", f"This user has {booking_count} bookings. Deleting the user will retain booking history. Continue?"):
                            self.db.close()
                            return
                
                # Delete the user
                cursor.execute("DELETE FROM Users WHERE UserID = ?", (user_id,))
                conn.commit()
                self.db.close()
                
                messagebox.showinfo("Success", f"User '{username}' deleted successfully!")
                self.load_users_data()  # Reload the users list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user: {e}")

    def setup_staff_tab(self, parent):
        """Set up the staff management tab"""
        # Staff tab is a filtered view of Users tab specifically for admin and manager roles
        
        # Staff list frame
        list_frame = tk.Frame(parent)
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Staff treeview
        columns = ("id", "name", "email", "role")
        self.staff_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        self.staff_tree.heading("id", text="ID")
        self.staff_tree.heading("name", text="Name")
        self.staff_tree.heading("email", text="Email")
        self.staff_tree.heading("role", text="Role")
        
        # Define column widths
        self.staff_tree.column("id", width=50)
        self.staff_tree.column("name", width=150)
        self.staff_tree.column("email", width=200)
        self.staff_tree.column("role", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.staff_tree.yview)
        self.staff_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        scrollbar.pack(side="right", fill="y")
        self.staff_tree.pack(fill="both", expand=True)
        
        # Load staff data
        self.load_staff_data()
        
        # Control frame
        control_frame = tk.Frame(parent)
        control_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        # Refresh button
        refresh_button = tk.Button(
            control_frame,
            text="Refresh List",
            width=15,
            command=self.load_staff_data
        )
        refresh_button.pack(pady=5)
        
        # Add staff button (redirects to add user)
        add_button = tk.Button(
            control_frame,
            text="Add Staff",
            width=15,
            command=lambda: self.add_staff_redirect()
        )
        add_button.pack(pady=5)

    def add_staff_redirect(self):
        """Redirect to add user dialog with staff role preselected"""
        # Create a new window
        add_window = tk.Toplevel(self)
        add_window.title("Add New Staff")
        add_window.geometry("400x350")
        add_window.resizable(False, False)
        
        # Get roles for dropdown
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT RoleID, RoleName FROM Roles WHERE RoleName IN ('Admin', 'Manager') ORDER BY RoleName")
        roles = cursor.fetchall()
        role_options = [f"{role['RoleName']}" for role in roles]
        self.db.close()
        
        # Username entry
        tk.Label(add_window, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        username_entry = tk.Entry(add_window, width=30)
        username_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Password entry
        tk.Label(add_window, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        password_entry = tk.Entry(add_window, width=30, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Confirm password entry
        tk.Label(add_window, text="Confirm Password:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        confirm_entry = tk.Entry(add_window, width=30, show="*")
        confirm_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Email entry
        tk.Label(add_window, text="Email:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        email_entry = tk.Entry(add_window, width=30)
        email_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Role selection
        tk.Label(add_window, text="Role:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        role_combo = ttk.Combobox(add_window, width=28, values=role_options, state="readonly")
        if role_options:
            role_combo.current(0)  # Default to first staff role
        role_combo.grid(row=4, column=1, padx=10, pady=5)
        
        # Add button
        tk.Button(
            add_window, 
            text="Add Staff", 
            command=lambda: self.add_staff(
                username_entry.get(),
                password_entry.get(),
                confirm_entry.get(),
                email_entry.get(),
                role_combo.get(),
                add_window
            )
        ).grid(row=5, column=0, columnspan=2, pady=20)

    def add_staff(self, username, password, confirm_password, email, role, window):
        """Add a new staff member"""
        # This is the same as add_user but will refresh both users and staff lists
        if not username or not password or not email or not role:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        # Email validation (simple check)
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        try:
            # Add the user
            success, message = self.db.create_user(username, password, email, role)
            
            if success:
                messagebox.showinfo("Success", f"Staff '{username}' added successfully!")
                window.destroy()
                self.load_users_data()  # Reload the users list
                self.load_staff_data()  # Reload the staff list
            else:
                messagebox.showerror("Error", message)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add staff: {e}")
    
    def load_staff_data(self):
        """Load staff data from database into treeview"""
        # Clear existing data
        for item in self.staff_tree.get_children():
            self.staff_tree.delete(item)
            
        try:
            # Connect to database - use local db instance
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Query to get staff data (users with Admin or Manager roles)
            cursor.execute("""
                SELECT 
                    u.UserID, 
                    u.Username as Name,
                    r.RoleName as Role,
                    u.Email as Contact
                FROM Users u
                JOIN Roles r ON u.RoleID = r.RoleID
                WHERE r.RoleName IN ('Admin', 'Manager')
                ORDER BY u.UserID
            """)
            
            staff = cursor.fetchall()
            
            # Insert data into treeview
            for person in staff:
                self.staff_tree.insert("", "end", values=(
                    person["UserID"],
                    person["Name"],
                    "All Locations", # Simplified until proper cinema assignment is implemented
                    person["Role"],
                    person["Contact"]
                ))
                
            if not staff:
                self.staff_tree.insert("", "end", values=("No staff accounts found", "", "", "", ""))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load staff data: {e}")
            self.staff_tree.insert("", "end", values=("Error loading data", "", "", "", ""))
        finally:
            self.db.close()  # Use local db