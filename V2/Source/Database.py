""" 
Database functions
"""
import sqlite3
import os
import hashlib
from datetime import datetime, timedelta

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
                FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
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
                FOREIGN KEY (FilmID) REFERENCES Films(FilmID) ON DELETE CASCADE,
                FOREIGN KEY (ScreenID) REFERENCES Screens(ScreenID) ON DELETE CASCADE
            );

            -- Customers who book tickets (could also reference Users)
            CREATE TABLE IF NOT EXISTS Customers (
                CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
                FullName TEXT NOT NULL,
                Email TEXT UNIQUE NOT NULL,
                PhoneNumber TEXT NOT NULL
            );

            -- Ticket bookings
            CREATE TABLE IF NOT EXISTS Bookings (
                BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
                CustomerID INTEGER NOT NULL,
                CinemaID INTEGER NOT NULL,
                ScreeningID INTEGER NOT NULL,
                BookingReference TEXT NOT NULL UNIQUE,
                TotalPrice REAL NOT NULL,
                BookingDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                Status TEXT DEFAULT 'active' CHECK(Status IN ('active', 'cancelled')),
                CancellationFee REAL DEFAULT 0,
                FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE,
                FOREIGN KEY (CinemaID) REFERENCES Cinemas(CinemaID) ON DELETE CASCADE,
                FOREIGN KEY (ScreeningID) REFERENCES Screenings(ScreeningID) ON DELETE CASCADE
            );

            -- Seats in each screen
            CREATE TABLE IF NOT EXISTS Seats (
                SeatID INTEGER PRIMARY KEY AUTOINCREMENT,
                ScreenID INTEGER NOT NULL,
                SeatNumber TEXT NOT NULL,
                SeatType TEXT NOT NULL CHECK(SeatType IN ('Lower Hall', 'Upper Gallery', 'VIP')),
                FOREIGN KEY (ScreenID) REFERENCES Screens(ScreenID) ON DELETE CASCADE
            );

            -- Individual seats booked within a booking
            CREATE TABLE IF NOT EXISTS BookingSeats (
                BookingSeatID INTEGER PRIMARY KEY AUTOINCREMENT,
                BookingID INTEGER NOT NULL,
                SeatID INTEGER NOT NULL,
                FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID) ON DELETE CASCADE,
                FOREIGN KEY (SeatID) REFERENCES Seats(SeatID) ON DELETE CASCADE,
                UNIQUE(BookingID, SeatID)
            );
        ''')
        
        # Insert default roles if they don't exist
        cursor.execute("INSERT OR IGNORE INTO Roles (RoleName) VALUES ('Admin')")
        cursor.execute("INSERT OR IGNORE INTO Roles (RoleName) VALUES ('Manager')")
        cursor.execute("INSERT OR IGNORE INTO Roles (RoleName) VALUES ('Customer')")
        
        # Create hardcoded admin user
        admin_password = "password1"  # As requested
        admin_password_hash = hashlib.sha256(admin_password.encode()).hexdigest()
        
        # Check if admin exists
        admin_exists = cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = 'admin'").fetchone()[0]
        
        if admin_exists:
            # Update the admin password to ensure it matches our hardcoded value
            cursor.execute(
                "UPDATE Users SET PasswordHash = ? WHERE Username = 'admin'",
                (admin_password_hash,)
            )
        else:
            # Create the admin user with our hardcoded credentials
            cursor.execute(
                "INSERT INTO Users (Username, PasswordHash, Email, RoleID) VALUES (?, ?, ?, ?)",
                ("admin", admin_password_hash, "admin@horizon.com", 1)
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
        
    def create_user(self, username, password, email, role="Customer"):
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
                "INSERT INTO Users (Username, PasswordHash, Email, RoleID) VALUES (?, ?, ?, ?)",
                (username, password_hash, email, role_id)
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
    
    def add_customer(self, full_name, email, phone_number=""):
        """Add a new customer to the database"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            # Check if customer already exists with this email
            existing = cursor.execute("SELECT CustomerID FROM Customers WHERE Email = ?", (email,)).fetchone()
            
            if existing:
                # Customer already exists, just return the ID
                customer_id = existing[0]
            else:
                # Insert new customer
                cursor.execute(
                    "INSERT INTO Customers (FullName, Email, PhoneNumber) VALUES (?, ?, ?)",
                    (full_name, email, phone_number)
                )
                conn.commit()
                customer_id = cursor.lastrowid
                
            self.close()
            return customer_id
        
        except Exception as e:
            conn.rollback()
            self.close()
            print(f"Error adding customer: {e}")
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
                    FOREIGN KEY (FilmID) REFERENCES Films(FilmID) ON DELETE CASCADE,
                    FOREIGN KEY (ScreenID) REFERENCES Screens(ScreenID) ON DELETE CASCADE
                );
            ''')

            # Check for duplicates and insert only new screenings
            for screening in screenings:
                film_id, screen_id, start_time, end_time, = screening
                cursor.execute('''
                    SELECT COUNT(*) FROM Screenings
                    WHERE FilmID = ? AND ScreenID = ? AND StartTime = ? AND EndTime = ?
                ''', (film_id, screen_id, start_time, end_time))
            
                if cursor.fetchone()[0] == 0:
                    cursor.execute('''
                        INSERT INTO Screenings (FilmID, ScreenID, StartTime, EndTime)
                        VALUES (?, ?, ?, ?)
                    ''', screening)

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
                SELECT ScreeningID, StartTime
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






