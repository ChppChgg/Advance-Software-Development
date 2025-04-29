"""
Manager page functions
"""
import tkinter as tk
from tkinter import ttk, messagebox
from Basepage import BasePage
from Database import Database  # Make sure this import is present

#Harry Elson, 23021935
#Matt Nogodula, 23015215
#Jerry Lin, 23024553

class ManagerPage(BasePage):
    """Manager page for system management"""
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
            text="Manager Dashboard",
            font=("Arial", 16, "bold"),
            bg="white"
        )
        page_title.pack(anchor="w", pady=(0, 20))
        
        # Tabs for different Manager functions
        tab_control = ttk.Notebook(content)
        
        # Screenings tab
        screenings_tab = ttk.Frame(tab_control)
        tab_control.add(screenings_tab, text="Screenings")
        
        # Users tab
        users_tab = ttk.Frame(tab_control)
        tab_control.add(users_tab, text="Users")
        
        cinemas_tab = ttk.Frame(tab_control)
        tab_control.add(cinemas_tab, text="Cinemas")
        
        # Screens tab
        screens_tab = ttk.Frame(tab_control)
        tab_control.add(screens_tab, text="Screens")
        
        tab_control.pack(expand=1, fill="both")
        
        # Set up tabs with data
        self.setup_screenings_tab(screenings_tab)
        self.setup_users_tab(users_tab)
        self.setup_cinemas_tab(cinemas_tab)
        self.setup_screens_tab(screens_tab)

    def setup_screenings_tab(self, parent):
        """Set up the screenings management tab"""
        # Screenings list frame
        list_frame = tk.Frame(parent)
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Screenings treeview - Add cinema column
        columns = ("id", "cinema", "film", "screen", "start_time", "end_time", "seats")
        self.screenings_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        self.screenings_tree.heading("id", text="ID")
        self.screenings_tree.heading("cinema", text="Cinema")  # New column
        self.screenings_tree.heading("film", text="Film")
        self.screenings_tree.heading("screen", text="Screen")
        self.screenings_tree.heading("start_time", text="Start Time")
        self.screenings_tree.heading("end_time", text="End Time")
        self.screenings_tree.heading("seats", text="Total Seats")
        
        # Define column widths
        self.screenings_tree.column("id", width=50)
        self.screenings_tree.column("cinema", width=150)  # New column
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
            
            # Query with cinema name from Screens-Cinemas relationship
            cursor.execute("""
                SELECT s.ScreeningID, f.Title, scr.ScreenNumber, s.StartTime, 
                       s.EndTime, s.TotalSeats, c.CinemaName
                FROM Screenings s
                JOIN Films f ON s.FilmID = f.FilmID
                JOIN Screens scr ON s.ScreenID = scr.ScreenID
                LEFT JOIN Cinemas c ON scr.CinemaID = c.CinemaID
                ORDER BY c.CinemaName, s.StartTime
            """)
            
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
            self.screenings_tree.insert("", "end", values=("Error loading data", "", "", "", "", "", ""))
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
    
    def setup_users_tab(self, parent):
        """Set up the users management tab"""
        # Users list frame
        list_frame = tk.Frame(parent)
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Add a new column for associated cinema
        columns = ("id", "username", "email", "role", "cinema")
        self.users_tree = ttk.Treeview(list_frame, columns=columns, show="headings")

        # Define headings
        self.users_tree.heading("id", text="ID")
        self.users_tree.heading("username", text="Username")
        self.users_tree.heading("email", text="Email")
        self.users_tree.heading("role", text="Role")
        self.users_tree.heading("cinema", text="Cinema")

        # Define column widths
        self.users_tree.column("id", width=50)
        self.users_tree.column("username", width=150)
        self.users_tree.column("email", width=200)
        self.users_tree.column("role", width=100)
        self.users_tree.column("cinema", width=150)
        
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
                    r.RoleName,
                    c.CinemaName
                FROM Users u
                JOIN Roles r ON u.RoleID = r.RoleID
                LEFT JOIN Cinemas c ON u.CinemaID = c.CinemaID
                ORDER BY u.UserID
            """)
            
            users = cursor.fetchall()
            
            # Insert data into treeview
            for user in users:
                self.users_tree.insert("", "end", values=(
                    user["UserID"],
                    user["Username"],
                    user["Email"],
                    user["RoleName"],
                    user["CinemaName"] if user["RoleName"].lower() == "staff" else ""
                ))
                
            if not users:
                self.users_tree.insert("", "end", values=("No users found", "", "", "", ""))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load users: {e}")
            self.users_tree.insert("", "end", values=("Error loading data", "", "", "", ""))
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
        if username.lower() == "Manager":
            messagebox.showerror("Error", "Cannot delete the Manager user")
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

    def setup_cinemas_tab(self, parent):
        """Set up the cinemas management tab"""
        # Cinemas list frame
        list_frame = tk.Frame(parent)
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Cinemas treeview
        columns = ("id", "name", "city", "address", "phone", "screens")
        self.cinemas_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        self.cinemas_tree.heading("id", text="ID")
        self.cinemas_tree.heading("name", text="Name")
        self.cinemas_tree.heading("city", text="City")
        self.cinemas_tree.heading("address", text="Address")
        self.cinemas_tree.heading("phone", text="Phone")
        self.cinemas_tree.heading("screens", text="Screens")
        
        # Define column widths
        self.cinemas_tree.column("id", width=40)
        self.cinemas_tree.column("name", width=180)
        self.cinemas_tree.column("city", width=100)
        self.cinemas_tree.column("address", width=150)
        self.cinemas_tree.column("phone", width=120)
        self.cinemas_tree.column("screens", width=60)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.cinemas_tree.yview)
        self.cinemas_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        scrollbar.pack(side="right", fill="y")
        self.cinemas_tree.pack(fill="both", expand=True)
        
        # Load cinema data
        self.load_cinemas_data()
        
        # Cinemas control frame
        control_frame = tk.Frame(parent)
        control_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        # Add cinema button
        add_button = tk.Button(
            control_frame,
            text="Add Cinema",
            width=15,
            command=self.show_add_cinema_dialog
        )
        add_button.pack(pady=5)
        
        # Edit cinema button
        edit_button = tk.Button(
            control_frame,
            text="Edit Cinema",
            width=15,
            command=self.show_edit_cinema_dialog
        )
        edit_button.pack(pady=5)
        
        # Delete cinema button
        delete_button = tk.Button(
            control_frame,
            text="Delete Cinema",
            width=15,
            command=self.delete_cinema
        )
        delete_button.pack(pady=5)
        
        # Refresh button
        refresh_button = tk.Button(
            control_frame,
            text="Refresh List",
            width=15,
            command=self.load_cinemas_data
        )
        refresh_button.pack(pady=5)
    
    def load_cinemas_data(self):
        """Load cinema data from database into treeview"""
        # Clear existing data
        for item in self.cinemas_tree.get_children():
            self.cinemas_tree.delete(item)
            
        try:
            # Get cinemas data from database
            cinemas = self.db.get_all_cinema_rows()
            
            # Insert into treeview
            for cinema in cinemas:
                self.cinemas_tree.insert("", "end", values=(
                    cinema["CinemaID"],
                    cinema["CinemaName"],
                    cinema["City"],
                    cinema["Address"],
                    cinema["Phone"],
                    cinema["NumberOfScreens"]
                ))
                
            if not cinemas:
                self.cinemas_tree.insert("", "end", values=("No cinemas found", "", "", "", "", ""))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load cinema data: {e}")
            self.cinemas_tree.insert("", "end", values=("Error loading data", "", "", "", "", ""))

    def show_add_cinema_dialog(self):
        """Show dialog to add a new cinema"""
        # Create a new window
        add_window = tk.Toplevel(self)
        add_window.title("Add New Cinema")
        add_window.geometry("400x350")
        add_window.resizable(False, False)
        
        # Cinema name entry
        tk.Label(add_window, text="Cinema Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        name_entry = tk.Entry(add_window, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # City entry
        tk.Label(add_window, text="City:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        city_entry = tk.Entry(add_window, width=30)
        city_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Address entry
        tk.Label(add_window, text="Address:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        address_entry = tk.Entry(add_window, width=30)
        address_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Phone entry
        tk.Label(add_window, text="Phone:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        phone_entry = tk.Entry(add_window, width=30)
        phone_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Number of screens
        tk.Label(add_window, text="Number of Screens:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        screens_var = tk.StringVar(value="6")
        screens_spinbox = ttk.Spinbox(
            add_window, 
            from_=1, 
            to=6, 
            textvariable=screens_var, 
            width=5
        )
        screens_spinbox.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        
        # Add button
        tk.Button(
            add_window, 
            text="Add Cinema", 
            command=lambda: self.add_cinema(
                name_entry.get(),
                city_entry.get(),
                address_entry.get(),
                phone_entry.get(),
                screens_var.get(),
                add_window
            )
        ).grid(row=5, column=0, columnspan=2, pady=20)

    def add_cinema(self, name, city, address, phone, num_screens, window):
        """Add a new cinema to the database"""
        # Validate inputs
        if not name or not city:
            messagebox.showerror("Error", "Cinema name and city are required")
            return
            
        try:
            num_screens = int(num_screens)
            if num_screens < 1 or num_screens > 6:
                messagebox.showerror("Error", "Number of screens must be between 1 and 6")
                return
                
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Check if cinema name already exists
            cursor.execute("SELECT COUNT(*) FROM Cinemas WHERE CinemaName = ?", (name,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "A cinema with this name already exists")
                self.db.close()
                return
                
            # Add the cinema
            cursor.execute(
                """
                INSERT INTO Cinemas (CinemaName, City, Address, Phone, NumberOfScreens)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, city, address, phone, num_screens)
            )
            
            conn.commit()
            self.db.close()
            
            messagebox.showinfo("Success", f"Cinema '{name}' added successfully!")
            window.destroy()
            self.load_cinemas_data()  # Reload the cinemas list
            
        except ValueError:
            messagebox.showerror("Error", "Number of screens must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add cinema: {e}")

    def show_edit_cinema_dialog(self):
        """Show dialog to edit selected cinema"""
        selected = self.cinemas_tree.selection()
        if not selected:
            messagebox.showinfo("Information", "Please select a cinema to edit")
            return
            
        # Get selected cinema data
        cinema_id = self.cinemas_tree.item(selected[0], "values")[0]
        
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Cinemas WHERE CinemaID = ?", (cinema_id,))
            cinema = cursor.fetchone()
            self.db.close()
            
            if not cinema:
                messagebox.showerror("Error", "Cinema not found in database")
                return
                
            # Create edit dialog window
            edit_window = tk.Toplevel(self)
            edit_window.title(f"Edit Cinema: {cinema['CinemaName']}")
            edit_window.geometry("400x350")
            edit_window.resizable(False, False)
            
            # Cinema name entry
            tk.Label(edit_window, text="Cinema Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            name_entry = tk.Entry(edit_window, width=30)
            name_entry.insert(0, cinema['CinemaName'])
            name_entry.grid(row=0, column=1, padx=10, pady=5)
            
            # City entry
            tk.Label(edit_window, text="City:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            city_entry = tk.Entry(edit_window, width=30)
            city_entry.insert(0, cinema['City'])
            city_entry.grid(row=1, column=1, padx=10, pady=5)
            
            # Address entry
            tk.Label(edit_window, text="Address:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
            address_entry = tk.Entry(edit_window, width=30)
            address_entry.insert(0, cinema['Address'] if cinema['Address'] else "")
            address_entry.grid(row=2, column=1, padx=10, pady=5)
            
            # Phone entry
            tk.Label(edit_window, text="Phone:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
            phone_entry = tk.Entry(edit_window, width=30)
            phone_entry.insert(0, cinema['Phone'] if cinema['Phone'] else "")
            phone_entry.grid(row=3, column=1, padx=10, pady=5)
            
            # Number of screens
            tk.Label(edit_window, text="Number of Screens:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
            screens_var = tk.StringVar(value=str(cinema['NumberOfScreens']))
            screens_spinbox = ttk.Spinbox(
                edit_window, 
                from_=1, 
                to=6, 
                textvariable=screens_var, 
                width=5
            )
            screens_spinbox.grid(row=4, column=1, padx=10, pady=5, sticky="w")
            
            # Update button
            tk.Button(
                edit_window, 
                text="Update Cinema", 
                command=lambda: self.update_cinema(
                    cinema_id,
                    name_entry.get(),
                    city_entry.get(),
                    address_entry.get(),
                    phone_entry.get(),
                    screens_var.get(),
                    edit_window
                )
            ).grid(row=5, column=0, columnspan=2, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load cinema data: {e}")

    def update_cinema(self, cinema_id, name, city, address, phone, num_screens, window):
        """Update an existing cinema in the database"""
        # Validate inputs
        if not name or not city:
            messagebox.showerror("Error", "Cinema name and city are required")
            return
            
        try:
            num_screens = int(num_screens)
            if num_screens < 1 or num_screens > 6:
                messagebox.showerror("Error", "Number of screens must be between 1 and 6")
                return
                
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Check if another cinema has this name
            cursor.execute("SELECT COUNT(*) FROM Cinemas WHERE CinemaName = ? AND CinemaID != ?", (name, cinema_id))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "Another cinema with this name already exists")
                self.db.close()
                return
                
            # Update the cinema
            cursor.execute(
                """
                UPDATE Cinemas 
                SET CinemaName = ?, City = ?, Address = ?, Phone = ?, NumberOfScreens = ?
                WHERE CinemaID = ?
                """,
                (name, city, address, phone, num_screens, cinema_id)
            )
            
            conn.commit()
            self.db.close()
            
            messagebox.showinfo("Success", f"Cinema '{name}' updated successfully!")
            window.destroy()
            self.load_cinemas_data()  # Reload the cinemas list
            
        except ValueError:
            messagebox.showerror("Error", "Number of screens must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update cinema: {e}")

    def delete_cinema(self):
        """Delete the selected cinema"""
        selected = self.cinemas_tree.selection()
        if not selected:
            messagebox.showinfo("Information", "Please select a cinema to delete")
            return
            
        # Get selected cinema data
        cinema_id = self.cinemas_tree.item(selected[0], "values")[0]
        cinema_name = self.cinemas_tree.item(selected[0], "values")[1]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{cinema_name}'?"):
            try:
                conn = self.db.connect()
                cursor = conn.cursor()
                
                # Check if cinema has any bookings
                cursor.execute("""
                    SELECT COUNT(*) FROM Bookings WHERE CinemaID = ?
                """, (cinema_id,))
                booking_count = cursor.fetchone()[0]
                
                if booking_count > 0:
                    if not messagebox.askyesno("Warning", f"This cinema has {booking_count} bookings. Deleting it will also delete all associated bookings. Continue?"):
                        self.db.close()
                        return
                
                # Delete the cinema (cascade will handle related records)
                cursor.execute("DELETE FROM Cinemas WHERE CinemaID = ?", (cinema_id,))
                conn.commit()
                self.db.close()
                
                messagebox.showinfo("Success", f"Cinema '{cinema_name}' deleted successfully!")
                self.load_cinemas_data()  # Reload the cinemas list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete cinema: {e}")
    
    def setup_screens_tab(self, parent):
        """Set up the screens management tab"""
        # Screens list frame
        list_frame = tk.Frame(parent)
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Screens treeview
        columns = ("id", "number", "capacity")
        self.screens_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        self.screens_tree.heading("id", text="ID")
        self.screens_tree.heading("number", text="Screen #")
        self.screens_tree.heading("capacity", text="Capacity")
        
        # Define column widths
        self.screens_tree.column("id", width=50)
        self.screens_tree.column("number", width=80)
        self.screens_tree.column("capacity", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.screens_tree.yview)
        self.screens_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        scrollbar.pack(side="right", fill="y")
        self.screens_tree.pack(fill="both", expand=True)
        
        # Screens control frame
        control_frame = tk.Frame(parent)
        control_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        # Add screen button
        add_button = tk.Button(
            control_frame,
            text="Add Screen",
            width=15,
            command=self.show_add_screen_dialog
        )
        add_button.pack(pady=5)
        
        # Edit screen button
        edit_button = tk.Button(
            control_frame,
            text="Edit Screen",
            width=15,
            command=self.show_edit_screen_dialog
        )
        edit_button.pack(pady=5)
        
        # Delete screen button
        delete_button = tk.Button(
            control_frame,
            text="Delete Screen",
            width=15,
            command=self.delete_screen
        )
        delete_button.pack(pady=5)
        
        # Load all screens initially
        self.load_all_screens()

    def load_all_screens(self):
        """Load all screens data"""
        # Clear existing data
        for item in self.screens_tree.get_children():
            self.screens_tree.delete(item)
            
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Query to get screen info
            cursor.execute("""
                SELECT ScreenID, ScreenNumber, SeatCapacity
                FROM Screens
                ORDER BY ScreenNumber
            """)
            
            screens = cursor.fetchall()
            self.db.close()
            
            # Insert data into treeview
            for screen in screens:
                self.screens_tree.insert("", "end", values=(
                    screen["ScreenID"],
                    screen["ScreenNumber"],
                    screen["SeatCapacity"]
                ))
                
            if not screens:
                self.screens_tree.insert("", "end", values=("No screens found", "", ""))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load screens: {e}")
            self.screens_tree.insert("", "end", values=("Error loading data", "", ""))

    def show_add_screen_dialog(self):
        """Show dialog to add a new screen"""
        # Create a new window
        add_window = tk.Toplevel(self)
        add_window.title("Add New Screen")
        add_window.geometry("350x250")
        add_window.resizable(False, False)
        
        # Get cinemas for dropdown
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT CinemaID, CinemaName FROM Cinemas ORDER BY CinemaName")
        cinemas = cursor.fetchall()
        cinema_options = [f"{cinema['CinemaID']} - {cinema['CinemaName']}" for cinema in cinemas]
        self.db.close()
        
        # Cinema selection
        tk.Label(add_window, text="Cinema:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        cinema_combo = ttk.Combobox(add_window, width=25, values=cinema_options, state="readonly")
        if cinema_options:
            cinema_combo.current(0)
        cinema_combo.grid(row=0, column=1, padx=10, pady=5)
        
        # Screen number
        tk.Label(add_window, text="Screen Number:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        number_var = tk.StringVar(value="1")
        number_spinbox = ttk.Spinbox(
            add_window, 
            from_=1, 
            to=10, 
            textvariable=number_var, 
            width=5
        )
        number_spinbox.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Seat capacity
        tk.Label(add_window, text="Seat Capacity:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        capacity_var = tk.StringVar(value="100")
        capacity_spinbox = ttk.Spinbox(
            add_window, 
            from_=50, 
            to=120, 
            textvariable=capacity_var, 
            width=5
        )
        capacity_spinbox.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        # Add button
        tk.Button(
            add_window, 
            text="Add Screen", 
            command=lambda: self.add_screen_with_cinema(
                cinema_combo.get().split(" - ")[0],
                number_var.get(),
                capacity_var.get(),
                add_window
            )
        ).grid(row=3, column=0, columnspan=2, pady=20)

    def add_screen_with_cinema(self, cinema_id, screen_number, capacity, window):
        """Add a new screen to the database with cinema association"""
        try:
            screen_number = int(screen_number)
            capacity = int(capacity)
            cinema_id = int(cinema_id)
            
            # Validate capacity range
            if capacity < 50 or capacity > 120:
                messagebox.showerror("Error", "Seat capacity must be between 50 and 120")
                return
                
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Check if screen number already exists in this cinema
            cursor.execute(
                "SELECT COUNT(*) FROM Screens WHERE ScreenNumber = ? AND CinemaID = ?", 
                (screen_number, cinema_id)
            )
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", f"Screen {screen_number} already exists in this cinema")
                self.db.close()
                return
                
            # Add the screen with cinema association
            cursor.execute(
                """
                INSERT INTO Screens (ScreenNumber, SeatCapacity, CinemaID)
                VALUES (?, ?, ?)
                """,
                (screen_number, capacity, cinema_id)
            )
            
            conn.commit()
            self.db.close()
            
            messagebox.showinfo("Success", f"Screen {screen_number} added successfully!")
            window.destroy()
            self.load_all_screens()  # Reload the screens list
            
        except ValueError:
            messagebox.showerror("Error", "Screen number and capacity must be numbers")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add screen: {e}")

    def show_edit_screen_dialog(self):
        """Show dialog to edit selected screen"""
        selected = self.screens_tree.selection()
        if not selected:
            messagebox.showinfo("Information", "Please select a screen to edit")
            return
        
        # Get selected screen data
        screen_id = self.screens_tree.item(selected[0], "values")[0]
        
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Screens WHERE ScreenID = ?", (screen_id,))
            screen = cursor.fetchone()
            self.db.close()
            
            if not screen:
                messagebox.showerror("Error", "Screen not found in database")
                return
                
            # Create edit dialog window
            edit_window = tk.Toplevel(self)
            edit_window.title(f"Edit Screen {screen['ScreenNumber']}")
            edit_window.geometry("350x200")
            edit_window.resizable(False, False)
            
            # Screen number
            tk.Label(edit_window, text="Screen Number:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            number_var = tk.StringVar(value=str(screen['ScreenNumber']))
            number_spinbox = ttk.Spinbox(
                edit_window, 
                from_=1, 
                to=10, 
                textvariable=number_var, 
                width=5
            )
            number_spinbox.grid(row=0, column=1, padx=10, pady=5, sticky="w")
            
            # Seat capacity
            tk.Label(edit_window, text="Seat Capacity:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            capacity_var = tk.StringVar(value=str(screen['SeatCapacity']))
            capacity_spinbox = ttk.Spinbox(
                edit_window, 
                from_=50, 
                to=120, 
                textvariable=capacity_var, 
                width=5
            )
            capacity_spinbox.grid(row=1, column=1, padx=10, pady=5, sticky="w")
            
            # Update button
            tk.Button(
                edit_window, 
                text="Update Screen", 
                command=lambda: self.update_screen(
                    screen_id,
                    number_var.get(),
                    capacity_var.get(),
                    edit_window
                )
            ).grid(row=2, column=0, columnspan=2, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load screen data: {e}")

    def update_screen(self, screen_id, screen_number, capacity, window):
        """Update an existing screen in the database"""
        try:
            screen_number = int(screen_number)
            capacity = int(capacity)
            
            # Validate capacity range
            if capacity < 50 or capacity > 120:
                messagebox.showerror("Error", "Seat capacity must be between 50 and 120")
                return
                
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Check if screen number already exists (excluding current screen)
            cursor.execute(
                "SELECT COUNT(*) FROM Screens WHERE ScreenNumber = ? AND ScreenID != ?", 
                (screen_number, screen_id)
            )
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", f"Screen {screen_number} already exists")
                self.db.close()
                return
                
            # Update the screen
            cursor.execute(
                """
                UPDATE Screens 
                SET ScreenNumber = ?, SeatCapacity = ?
                WHERE ScreenID = ?
                """,
                (screen_number, capacity, screen_id)
            )
            
            conn.commit()
            self.db.close()
            
            messagebox.showinfo("Success", f"Screen deleted successfully!")
            window.destroy()
            self.load_all_screens()  # Reload the screens list
            
        except ValueError:
            messagebox.showerror("Error", "Screen number and capacity must be numbers")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update screen: {e}")

    def delete_screen(self):
        """Delete the selected screen"""
        selected = self.screens_tree.selection()
        if not selected:
            messagebox.showinfo("Information", "Please select a screen to delete")
            return
            
        # Get selected screen data
        screen_id = self.screens_tree.item(selected[0], "values")[0]
        screen_number = self.screens_tree.item(selected[0], "values")[1]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Screen {screen_number}?"):
            try:
                conn = self.db.connect()
                cursor = conn.cursor()
                
                # Check if screen has any screenings
                cursor.execute("SELECT COUNT(*) FROM Screenings WHERE ScreenID = ?", (screen_id,))
                screening_count = cursor.fetchone()[0]
                
                if screening_count > 0:
                    if not messagebox.askyesno("Warning", f"This screen has {screening_count} screenings scheduled. Deleting it will also delete all associated screenings and bookings. Continue?"):
                        self.db.close()
                        return
                
                # Delete the screen (cascade will handle related records)
                cursor.execute("DELETE FROM Screens WHERE ScreenID = ?", (screen_id,))
                conn.commit()
                self.db.close()
                
                messagebox.showinfo("Success", f"Screen deleted successfully!")
                self.load_all_screens()  # Reload the screens list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete screen: {e}")