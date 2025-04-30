"""
Admin page 
"""
import tkinter as tk
from tkinter import ttk, messagebox
from Basepage import BasePage
from Database import Database
import sqlite3

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
        
        films_tab = ttk.Frame(tab_control)
        tab_control.add(films_tab, text="Films")

        reports_tab = ttk.Frame(tab_control)
        tab_control.add(reports_tab, text="Reports")

        
        tab_control.pack(expand=1, fill="both")
        
        self.setup_films_tab(films_tab)
        self.setup_reports_tab(reports_tab)

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
            self.db.close()

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