"""
Manager page 
"""
import tkinter as tk
from tkinter import ttk, messagebox
from Basepage import BasePage
from Database import Database
import sqlite3

#Harry Elson, 23021935
#Matt Nogodula, 23015215
#Jerry Lin, 23024553

class ManagerPage(BasePage):
    """Manager page for cinema management"""
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
            text="Cinema Manager Dashboard",
            font=("Arial", 16, "bold"),
            bg="white"
        )
        page_title.pack(anchor="w", pady=(0, 20))
        
        # Tabs for different manager functions
        tab_control = ttk.Notebook(content)
        
        # Cinemas tab
        cinemas_tab = ttk.Frame(tab_control)
        tab_control.add(cinemas_tab, text="Cinemas")
        
        # Screens tab
        screens_tab = ttk.Frame(tab_control)
        tab_control.add(screens_tab, text="Screens")
        
        tab_control.pack(expand=1, fill="both")
        
        # Cinemas tab content
        self.setup_cinemas_tab(cinemas_tab)
        
        # Screens tab content
        self.setup_screens_tab(screens_tab)
    
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
        add_window.geometry("350x200")
        add_window.resizable(False, False)
        
        # Screen number
        tk.Label(add_window, text="Screen Number:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        number_var = tk.StringVar(value="1")
        number_spinbox = ttk.Spinbox(
            add_window, 
            from_=1, 
            to=10, 
            textvariable=number_var, 
            width=5
        )
        number_spinbox.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Seat capacity
        tk.Label(add_window, text="Seat Capacity:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        capacity_var = tk.StringVar(value="100")
        capacity_spinbox = ttk.Spinbox(
            add_window, 
            from_=50, 
            to=120, 
            textvariable=capacity_var, 
            width=5
        )
        capacity_spinbox.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Add button
        tk.Button(
            add_window, 
            text="Add Screen", 
            command=lambda: self.add_screen(
                number_var.get(),
                capacity_var.get(),
                add_window
            )
        ).grid(row=2, column=0, columnspan=2, pady=20)

    def add_screen(self, screen_number, capacity, window):
        """Add a new screen to the database"""
        try:
            screen_number = int(screen_number)
            capacity = int(capacity)
            
            # Validate capacity range
            if capacity < 50 or capacity > 120:
                messagebox.showerror("Error", "Seat capacity must be between 50 and 120")
                return
                
            conn = self.db.connect()
            cursor = conn.cursor()
            
            # Check if screen number already exists
            cursor.execute(
                "SELECT COUNT(*) FROM Screens WHERE ScreenNumber = ?", 
                (screen_number,)
            )
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", f"Screen {screen_number} already exists")
                self.db.close()
                return
                
            # Add the screen
            cursor.execute(
                """
                INSERT INTO Screens (ScreenNumber, SeatCapacity)
                VALUES (?, ?)
                """,
                (screen_number, capacity)
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
            
            messagebox.showinfo("Success", f"Screen updated successfully!")
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