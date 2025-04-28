""" 
Database functions
"""
import sqlite3
import os
import uuid
import hashlib
from datetime import datetime, timedelta

#Harry Elson, 23021935
#Matt Nogodula, 23015215
#Jerry Lin, 23024553

class Database:
    """Database manager class for Horizon Cinemas"""
    
    def __init__(self, db_name="horizon_cinemas.db"):
        """Initialize database connection"""
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.connection = None
        self.create_tables()
        
    def connect(self):
        """Create a database connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Enable row access by column name
        return self.connection
        
    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            
    def create_tables(self):
        """Create all database tables if they don't exist"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Create tables
        cursor.executescript('''
            -- Roles for user access control
            CREATE TABLE IF NOT EXISTS Roles (
                RoleID INTEGER PRIMARY KEY AUTOINCREMENT,
                RoleName TEXT NOT NULL UNIQUE
            );

            -- Users for system authentication
            CREATE TABLE IF NOT EXISTS Users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL UNIQUE,
                PasswordHash TEXT NOT NULL,
                Email TEXT UNIQUE NOT NULL,
                RoleID INTEGER NOT NULL,
                CinemaID INTEGER NOT NULL,
                FOREIGN KEY (RoleID) REFERENCES Roles(RoleID) ON DELETE CASCADE,
                FOREIGN KEY (CinemaID) REFERENCES Cinemas(CinemaID) ON DELETE CASCADE
            );

            -- Cinemas located in different cities
            CREATE TABLE IF NOT EXISTS Cinemas (
                CinemaID INTEGER PRIMARY KEY AUTOINCREMENT,
                CinemaName TEXT NOT NULL,
                City TEXT NOT NULL,
                Address TEXT,
                Phone TEXT,
                NumberOfScreens INTEGER NOT NULL CHECK(NumberOfScreens <= 6)
            );

            -- Screens within each cinema
            CREATE TABLE IF NOT EXISTS Screens (
                ScreenID INTEGER PRIMARY KEY AUTOINCREMENT,
                ScreenNumber INTEGER NOT NULL,
                SeatCapacity INTEGER NOT NULL CHECK(SeatCapacity BETWEEN 50 AND 120)
            );

            -- Films available for screenings
            CREATE TABLE IF NOT EXISTS Films (
                FilmID INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT NOT NULL,
                Description TEXT,
                Actors TEXT,
                Genre TEXT,
                Rating TEXT,
                Duration INTEGER NOT NULL -- in minutes
            );

            -- Scheduled screenings for films
            CREATE TABLE IF NOT EXISTS Screenings (
                ScreeningID INTEGER PRIMARY KEY AUTOINCREMENT,
                FilmID INTEGER NOT NULL,
                ScreenID INTEGER NOT NULL,
                StartTime TIME NOT NULL,
                EndTime TIME NOT NULL,
                TotalSeats INTEGER NOT NULL,
                VIPSeats INTEGER NOT NULL DEFAULT 10,
                LowerSeats INTEGER NOT NULL,
                UpperSeats INTEGER NOT NULL,
                FOREIGN KEY (TotalSeats) REFERENCES Screens(SeatCapacity) ON DELETE CASCADE,
                FOREIGN KEY (FilmID) REFERENCES Films(FilmID) ON DELETE CASCADE,
                FOREIGN KEY (ScreenID) REFERENCES Screens(ScreenID) ON DELETE CASCADE         
            );

            --  Staff who book tickets (could also reference Users)
            CREATE TABLE IF NOT EXISTS Staff (
                StaffID INTEGER PRIMARY KEY AUTOINCREMENT,
                FullName Text NOT NULL,
                Email TEXT UNIQUE NOT NULL
            );

            -- Ticket bookings
            CREATE TABLE IF NOT EXISTS Bookings (
                BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
                StaffID INTEGER NOT NULL,
                CinemaID INTEGER NOT NULL,
                ScreeningID INTEGER NOT NULL,
                BookingReference TEXT NOT NULL UNIQUE,
                TotalPrice REAL NOT NULL,
                BookingDate DATE NOT NULL,
                Status TEXT DEFAULT 'active' CHECK(Status IN ('active', 'cancelled')),
                CancellationFee REAL DEFAULT 0,
                FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE CASCADE,
                FOREIGN KEY (CinemaID) REFERENCES Cinemas(CinemaID) ON DELETE CASCADE,
                FOREIGN KEY (ScreeningID) REFERENCES Screenings(ScreeningID) ON DELETE CASCADE
            );

            -- Individual seats booked within a booking
            CREATE TABLE IF NOT EXISTS BookingSeats (
                BookingSeatID INTEGER PRIMARY KEY AUTOINCREMENT,
                BookingID INTEGER NOT NULL,
                SeatType TEXT NOT NULL CHECK (SeatType IN ('VIP', 'Lower', 'Upper')),
                FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID) ON DELETE CASCADE
            );

        ''')
        
        # Insert default roles if they don't exist
        cursor.execute("INSERT OR IGNORE INTO Roles (RoleName) VALUES ('Admin')")
        cursor.execute("INSERT OR IGNORE INTO Roles (RoleName) VALUES ('Manager')")
        cursor.execute("INSERT OR IGNORE INTO Roles (RoleName) VALUES ('Staff')")
        
        # Create hardcoded admin user
        admin_password = "password1" 
        admin_password_hash = hashlib.sha256(admin_password.encode()).hexdigest()

        manager_password = "password1" 
        manager_password_hash = hashlib.sha256(manager_password.encode()).hexdigest()
        
        # Check if admin exists
        admin_exists = cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = 'admin'").fetchone()[0]
        manager_exists = cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = 'manager'").fetchone()[0]
        
        if admin_exists:
            # Update the admin password to ensure it matches our hardcoded value
            cursor.execute(
                "UPDATE Users SET PasswordHash = ? WHERE Username = 'admin'",
                (admin_password_hash,)
            )
        else:
            # Get the Admin role ID
            cursor.execute("SELECT RoleID FROM Roles WHERE RoleName = 'Admin'")
            admin_role_id = cursor.fetchone()[0]
            
            # Create the admin user with the Admin role
            cursor.execute(
                "INSERT INTO Users (Username, PasswordHash, Email, RoleID,  CinemaID) VALUES (?, ?, ?, ?, ?)",
                ("admin", admin_password_hash, "admin@horizon.com", admin_role_id, 1)
            )
        
        if manager_exists:
            # Update the manager password AND role to ensure they're correct
            cursor.execute("SELECT RoleID FROM Roles WHERE RoleName = 'Manager'")
            manager_role_id = cursor.fetchone()[0]
            
            cursor.execute(
                "UPDATE Users SET PasswordHash = ?, RoleID = ? WHERE Username = 'manager'",
                (manager_password_hash, manager_role_id)
            )
        else:
            # Get the Manager role ID
            cursor.execute("SELECT RoleID FROM Roles WHERE RoleName = 'Manager'")
            manager_role_id = cursor.fetchone()[0]
            
            # Create the manager user with the Manager role
            cursor.execute(
                "INSERT INTO Users (Username, PasswordHash, Email, RoleID, CinemaID) VALUES (?, ?, ?, ?, ?)",
                ("manager", manager_password_hash, "manager@horizon.com", manager_role_id, 1)
            )
        
        conn.commit()
        self.close()
        
    def authenticate_user(self, username, password):
        """Authenticate a user by username and password"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Hash the password for comparison
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Query for user with matching credentials
        user = cursor.execute(
            """
            SELECT u.UserID, u.Username, r.RoleName 
            FROM Users u
            JOIN Roles r ON u.RoleID = r.RoleID
            WHERE u.Username = ? AND u.PasswordHash = ?
            """, 
            (username, password_hash)
        ).fetchone()
        
        self.close()
        return user if user else None
        
    def create_user(self, username, password, email, cinema_id, role='Staff'):
        """Create a new user"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            # Get role ID
            role_id = cursor.execute("SELECT RoleID FROM Roles WHERE RoleName = ?", (role,)).fetchone()
            
            if not role_id:
                conn.close()
                return False, "Invalid role"
                
            role_id = role_id[0]
            
            # Hash the password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Insert the new user
            cursor.execute(
                "INSERT INTO Users (Username, PasswordHash, Email, CinemaID, RoleID) VALUES (?, ?, ?, ?, ?)",
                (username, password_hash, email, cinema_id, role_id)
            )
            
            conn.commit()
            self.close()
            return True, "User created successfully"
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            self.close()
            if "UNIQUE constraint failed: Users.Username" in str(e):
                return False, "Username already exists"
            elif "UNIQUE constraint failed: Users.Email" in str(e):
                return False, "Email already exists"
            else:
                return False, f"Database error: {e}"
                
        except Exception as e:
            conn.rollback()
            self.close()
            return False, f"Error: {e}"
    
    def add_staff(self, full_name, email):
        """Add a new staff to the database"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            # Check if staff member already exists with this email
            existing = cursor.execute("SELECT StaffID FROM Staff WHERE Email = ?", (email,)).fetchone()
            
            if existing:
                # staff already exists, just return the ID
                staff_id = existing[0]
            else:
                # Insert new staff
                cursor.execute(
                    "INSERT INTO Staff (FullName, Email) VALUES (?, ?)",
                    (full_name, email)
                )
                conn.commit()
                staff_id = cursor.lastrowid
                
            self.close()
            return staff_id
        
        except Exception as e:
            conn.rollback()
            self.close()
            print(f"Error adding staff: {e}")
            return None

    def add_film(self, title, description, actors, genre, rating, duration):
        """Add a new film to the database"""
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO Films (Title, Description, Actors, Genre, Rating, Duration)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (title, description, actors, genre, rating, duration)
            )
            conn.commit()
            film_id = cursor.lastrowid
            self.close()
            return film_id
        except Exception as e:
            conn.rollback()
            self.close()
            print(f"Error adding film: {e}")
            return None

    def get_all_film_rows(self):
        """Fetch all film records from the database."""
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Films")
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("Error fetching films:", e)
            return []
        finally:
            self.close()
    
    def generate_cinemas(self):
        cinemas = [
            ("Bristol Cinema","Bristol", "BS2 0SP","01496 222750",6),
            ("Filton Cinema", "Bristol", "BS16 1QY","01496 222850", 6),
            ("Cardiff Cinema","Cardiff", "CF10 1LA", "01496 222950", 6),
            ("Cardiff Bay Cinema","Cardiff", "CF64 1TQ", "01496 222050",6),
            ("Birmingham Cinema","Birmingham","B16 8LP", "01496 222150", 6),
            ("Birmingham Broad Street Cinema", "Birmingham", "B15 1DA", "01496 222250", 6),
            ("London Paddington Cinema", "London", "W2 1HQ", "01496 222350",6),
            ("London Victoria Cinema", "London", "SW1V 1JU", "01496 222450",6)
        ]
        
        try: 
            self.connect()
            cursor = self.connection.cursor()
            
            # Create the table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Cinemas (
                CinemaID INTEGER PRIMARY KEY AUTOINCREMENT,
                CinemaName TEXT NOT NULL,
                City TEXT NOT NULL,
                Address TEXT,
                Phone TEXT,
                NumberOfScreens INTEGER NOT NULL CHECK(NumberOfScreens <= 6)
                )
            ''')

            # Check for duplicates and insert only new cinemas
            for cinema in cinemas:
                cursor.execute("SELECT COUNT(*) FROM Cinemas WHERE CinemaName = ?", (cinema[0],))
                if cursor.fetchone()[0] == 0:
                    cursor.execute('''
                        INSERT INTO Cinemas (CinemaName, City, Address, Phone, NumberOfScreens)
                        VALUES (?, ?, ?, ?, ?)
                    ''', cinema)

            self.connection.commit()
            print("Cinemas inserted successfully.")
            
        except Exception as e:
            print("Error inserting films:", e)
        finally:
            self.close()
            

    def insert_initial_films(self):
        """Insert predefined films into the Films table if they don't already exist."""
        films_to_add = [
            ("A Minecraft Movie", "Four misfits are suddenly pulled through a mysterious portal into a bizarre cubic wonderland that thrives on imagination. To get back home they'll have to master this world while embarking on a quest with an unexpected expert crafter.", "Jack Black, Jason Mamoa, Sebastian Hansen", "Comedy", "PG", 101),
            ("The Amateur", "When a CIA cryptographer discovers that terrorists were behind his fiancée's death in a suspicious plane crash, he receives special training in order to plot his revenge.", "Rami Malek, Rachel Brosnahan, Caitriona Balfe, Julianne Nicholson, Holt McCallany", "Spy", "12A", 122),
            ("DROP", "First dates are nerve-wracking enough. Going on a first date while an unnamed unseen troll pings you personal memes that escalate from annoying to homicidal?", "Meghann Fahy, Brandon Sklenar, Violett Beane, Jacob Robinson, Ed Weeks, Jeffery Self", "Thriller", "15", 95),
            ("Death of a Unicorn", "Father-Daughter duo, Riley and Elliot, hit a unicorn with their car and bring it to the wilderness retreat of a mega-wealthy pharmaceutical CEO.", "Paul Rudd, Jenna Ortega, Téa Leoni, Will Poulter, Richard E Grant", "Comedy / Horror", "15", 107),
            ("Star Wars: Episode III - Revenge of the Sith (20th anniversary)", "Three years into the Clone Wars, the Jedi rescue Palpatine from Count Dooku. As Obi-Wan pursues a new threat, Anakin acts as a double agent...", "Christopher Lee, Natalie Portman, Hayden Christensen, Ian McDiarmid, Frank Oz, Ewan McGregor, Samuel L. Jackson, Anthony Daniels, Kenny Baker", "Sci-Fi", "12A", 140)
        ]
        
        try:
            self.connect()
            cursor = self.connection.cursor()
            
            # Create the table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Films (
                FilmID INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT NOT NULL,
                Description TEXT,
                Actors TEXT,
                Genre TEXT,
                Rating TEXT,
                Duration INTEGER NOT NULL -- in minutes
                )
            ''')
            
            # Check for duplicates and insert only new titles
            for film in films_to_add:
                cursor.execute("SELECT COUNT(*) FROM Films WHERE title = ?", (film[0],))
                if cursor.fetchone()[0] == 0:
                    cursor.execute('''
                        INSERT INTO Films (Title, Description, Actors, Genre, Rating, Duration)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', film)

            self.connection.commit()
            print("Films inserted successfully.")
            
        except Exception as e:
            print("Error inserting films:", e)
        finally:
            self.close()
    
    def populate_screens(self):
        screens = [
            ("1", "120"),
            ("2", "100"),
            ("3", "100"),
            ("4", "80"),
            ("5", "80"),
            ("6", "60")
        ]

        try:
            self.connect()
            cursor = self.connection.cursor()
            
            # Create the table if it doesn't exist
            cursor.execute('''

            ''')
            
            # Check for duplicates and insert only new titles
            for screen in screens:
                cursor.execute("SELECT COUNT(*) FROM Screens WHERE ScreenNumber = ?", (screen[0],))
                if cursor.fetchone()[0] == 0:
                    cursor.execute('''
                        INSERT INTO Screens (ScreenNumber, SeatCapacity)
                        VALUES (?, ?)
                    ''', screen)

            self.connection.commit()
            print("Screens inserted successfully.")
            
        except Exception as e:
            print("Error inserting films:", e)
        finally:
            self.close()

    def initial_screenings(self):
        screenings = [
            (1, 1, "09:00", "11:00"),
            (6, 1, "11:00", "13:30"),
            (2, 1, "13:30", "16:00"),
            (3, 1, "16:00", "18:00"),
            (5, 1, "18:00", "20:00"),
            (4, 1, "20:00", "22:00"),
            (1, 2, "11:00", "13:00"),
            (6, 2, "13:00", "15:30"),
            (2, 2, "15:30", "18:00"),
            (3, 2, "18:00", "20:00"),
            (5, 2, "20:00", "22:00"),
            (4, 2, "22:00", "00:00"),
            (4, 3, "09:00", "11:00"),
            (1, 3, "13:00", "15:00"),
            (6, 3, "15:00", "17:30"),
            (2, 3, "17:30", "20:00"),
            (3, 3, "20:00", "22:00"),
            (5, 3, "22:00", "00:00"),
            (5, 4, "09:00", "11:00"),
            (4, 4, "11:00", "13:00"),
            (1, 4, "15:00", "17:00"),
            (6, 4, "17:00", "19:30"),
            (2, 4, "19:30", "22:00"),
            (3, 4, "22:00", "00:00"),
            (3, 5, "09:00", "11:00"),
            (5, 5, "11:00", "13:00"),
            (4, 5, "13:00", "15:00"),
            (1, 5, "17:00", "19:00"),
            (6, 5, "19:00", "21:30"),
            (2, 5, "21:30", "00:00"),
            (2, 6, "09:00", "11:30"),
            (3, 6, "11:30", "13:30"),
            (5, 6, "13:30", "15:30"),
            (4, 6, "15:30", "17:30"),
            (1, 6, "19:30", "21:30"),
            (6, 6, "21:30", "00:00")
        ]

        try:
            self.connect()
            cursor = self.connection.cursor()

            # Create the table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Screenings (
                    ScreeningID INTEGER PRIMARY KEY AUTOINCREMENT,
                    FilmID INTEGER NOT NULL,
                    ScreenID INTEGER NOT NULL,
                    StartTime TIME NOT NULL,
                    EndTime TIME NOT NULL,
                    TotalSeats INTEGER NOT NULL,
                    VIPSeats INTEGER NOT NULL DEFAULT 10,
                    LowerSeats INTEGER NOT NULL,
                    UpperSeats INTEGER NOT NULL,
                    FOREIGN KEY (TotalSeats) REFERENCES Screens(SeatCapacity) ON DELETE CASCADE,
                    FOREIGN KEY (FilmID) REFERENCES Films(FilmID) ON DELETE CASCADE,
                    FOREIGN KEY (ScreenID) REFERENCES Screens(ScreenID) ON DELETE CASCADE
                );
            ''')

            for film_id, screen_id, start_time, end_time in screenings:
                # Get the total seat capacity for this screen
                cursor.execute("SELECT SeatCapacity FROM Screens WHERE ScreenID = ?", (screen_id,))
                result = cursor.fetchone()
                if not result:
                    print(f"ScreenID {screen_id} not found, skipping.")
                    continue

                total_seats = result[0]
                vip_seats = 10
                lower_seats = int(total_seats * 0.3)
                upper_seats = total_seats - vip_seats - lower_seats

                # Check for duplicate screening
                cursor.execute('''
                    SELECT COUNT(*) FROM Screenings
                    WHERE FilmID = ? AND ScreenID = ? AND StartTime = ? AND EndTime = ?
                ''', (film_id, screen_id, start_time, end_time))

                if cursor.fetchone()[0] == 0:
                    cursor.execute('''
                        INSERT INTO Screenings (FilmID, ScreenID, StartTime, EndTime, TotalSeats, VIPSeats, LowerSeats, UpperSeats)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (film_id, screen_id, start_time, end_time, total_seats, vip_seats, lower_seats, upper_seats))

            self.connection.commit()
            print("Screenings inserted successfully.")

        except Exception as e:
            print("Error inserting screenings:", e)
        finally:
            self.close()

    def get_screenings_by_film(self, film_id):
        """Fetch screening start times by film ID."""
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = """
                SELECT ScreeningID, ScreenID, StartTime
                FROM Screenings
                WHERE FilmID = ?
                ORDER BY StartTime
            """
            cursor.execute(query, (film_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            print("Error fetching screenings:", e)
            return []
        finally:
            self.close()
    
    def get_all_cinema_rows(self):
        """Fetch all film records from the database."""
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Cinemas")
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("Error fetching Cinemas:", e)
            return []
        finally:
            self.close()

    def insert_booking(self, staff_id, cinema_id, screening_id, booking_ref, total_price, cancellationfee, bookingdate, status):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO Bookings (
                    StaffID,
                    CinemaID,
                    ScreeningID,
                    BookingReference,
                    TotalPrice,
                    BookingDate,
                    Status,
                    CancellationFee
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (staff_id, cinema_id, screening_id, booking_ref, total_price, bookingdate, status, cancellationfee))
            booking_id = cursor.lastrowid
            self.connection.commit()
        except Exception as e:
            print("Error inserting booking:", e)
            return []
        finally:
            self.close()
            return booking_id
    
    def get_booked_seat_counts(self, screening_id, booking_date):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT SeatType, COUNT(*) as Count
            FROM BookingSeats bs
            JOIN Bookings b ON b.BookingID = bs.BookingID
            WHERE b.ScreeningID = ? AND b.BookingDate = ? AND b.Status = 'active'
            GROUP BY SeatType
        """, (screening_id, booking_date))
        
        results = cursor.fetchall()
        self.close()

        # Convert to dictionary like {'VIP': 5, 'Lower': 12, 'Upper': 30}
        return {row[0]: row[1] for row in results}
    
    def insert_booking_seat(self, booking_id, seat_type):
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO BookingSeats (BookingID, SeatType)
                VALUES (?, ?)
            """, (booking_id, seat_type))
            self.connection.commit()
            self.close()

    def get_screen_info(self, screen_id):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Screens WHERE ScreenID = ?", (screen_id,))
        result = cursor.fetchone()
        self.close()
        return dict(result) if result else None

    def get_email_by_username(self,username):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT email FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        self.close()
        return result[0] if result else None
    
    def get_cinema_id_by_username(self, username):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT CinemaID FROM Users WHERE Username = ?", (username,))
        row = cursor.fetchone()
        return row['CinemaID'] if row else None

    def get_staff_id_by_email(self, email):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT StaffID FROM Staff WHERE Email = ?", (email,))
        row = cursor.fetchone()
        return row[0] if row else None

    def get_bookings_by_staff_id(self, staff_id):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT 
                b.BookingReference,
                f.Title,
                b.BookingDate,
                s.StartTime,
                COUNT(bs.BookingSeatID) as SeatCount,
                b.Status
            FROM Bookings b
            JOIN Screenings s ON b.ScreeningID = s.ScreeningID
            JOIN Films f ON s.FilmID = f.FilmID
            LEFT JOIN BookingSeats bs ON b.BookingID = bs.BookingID
            WHERE b.StaffID = ?
            GROUP BY b.BookingID
            ORDER BY b.BookingDate DESC
        """, (staff_id,))
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def cancel_booking_by_reference(self, booking_ref):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE Bookings
            SET Status = 'cancelled'
            WHERE BookingReference = ? AND Status != 'cancelled'
        """, (booking_ref,))
        self.connection.commit()
        return cursor.rowcount > 0  # Returns True if a row was updated

    def get_cancellation_fee(self, booking_ref):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT CancellationFee FROM Bookings
            WHERE BookingReference = ?
        """, (booking_ref,))
        row = cursor.fetchone()
        self.close()
        return row[0] if row else None
    
    def get_booking_info_by_reference(self, booking_ref):
        self.connect()
        cursor = self.connection.cursor()
        self.connection.row_factory = sqlite3.Row 


        cursor.execute("""
            SELECT BookingDate, CancellationFee, Status
            FROM Bookings
            WHERE BookingReference = ?
        """, (booking_ref,))
        result = cursor.fetchone()

        self.close()
        return dict(result) if result else None

    def get_all_cinemas(self):
        """Fetch all cinema records from the database."""
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Cinemas")  # Adjust table name if needed
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("Error fetching cinemas:", e)
            return []
        finally:
            self.close()

    def get_user_role_by_username(self, username):
        """Get the role of the user (admin, manager, or staff) by their username."""
        self.connect()
        cursor = self.connection.cursor()

        # Query to get RoleID for the given username
        cursor.execute("SELECT RoleID FROM Users WHERE Username = ?", (username,))
        row = cursor.fetchone()

        if row is None:
            return None

        # Get the RoleID from the query result
        role_id = row['RoleID']

        # Query to get the role name based on RoleID
        cursor.execute("SELECT RoleName FROM Roles WHERE RoleID = ?", (role_id,))
        role_row = cursor.fetchone()

        # Return the role name, if found, otherwise None
        return role_row['RoleName'] if role_row else None





