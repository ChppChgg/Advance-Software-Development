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
        self.connection.row_factory = sqlite3.Row  
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

            -- Screens within each cinema - Modified to include CinemaID
            CREATE TABLE IF NOT EXISTS Screens (
                ScreenID INTEGER PRIMARY KEY AUTOINCREMENT,
                ScreenNumber INTEGER NOT NULL,
                SeatCapacity INTEGER NOT NULL CHECK(SeatCapacity BETWEEN 50 AND 120),
                CinemaID INTEGER NOT NULL,
                FOREIGN KEY (CinemaID) REFERENCES Cinemas(CinemaID) ON DELETE CASCADE
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

            --  Customers who book tickets 
            CREATE TABLE IF NOT EXISTS Customers (
                CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
                FullName Text NOT NULL,
                Email TEXT NOT NULL
            );

            -- Ticket bookings
            CREATE TABLE IF NOT EXISTS Bookings (
                BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NOT NULL,
                CustomerID INTEGER NOT NULL,
                CinemaID INTEGER NOT NULL,
                ScreeningID INTEGER NOT NULL,
                BookingReference TEXT NOT NULL UNIQUE,
                TotalPrice REAL NOT NULL,
                BookingDate DATE NOT NULL,
                Status TEXT DEFAULT 'active' CHECK(Status IN ('active', 'cancelled')),
                CancellationFee REAL DEFAULT 0,
                FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
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
    
    def add_customer(self, full_name, email):
        """Add a new customer to the database"""
        conn = self.connect()
        cursor = conn.cursor()
        
    
        # Check if customer with the same full name already exists
        cursor.execute("SELECT CustomerID FROM Customers WHERE FullName = ?", (full_name,))
        existing_customer = cursor.fetchone()

        if existing_customer:
            # If customer with the same full name exists, return their CustomerID
            return existing_customer[0]
        
        # Insert new customer
        cursor.execute(
                "INSERT INTO Customers (FullName, Email) VALUES (?, ?)",
                (full_name, email)
            )
        conn.commit()
        customer_id = cursor.lastrowid
            
        self.close()
        return customer_id
        

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
        try:
            self.connect()
            cursor = self.connection.cursor()
            
            # Get all cinemas
            cursor.execute("SELECT CinemaID FROM Cinemas")
            cinemas = cursor.fetchall()
            
            if not cinemas:
                print("No cinemas found. Please add cinemas first.")
                return
            
            # For each cinema, create 6 screens
            for cinema in cinemas:
                cinema_id = cinema['CinemaID']
                
                screens = [
                    (1, 120, cinema_id),
                    (2, 100, cinema_id),
                    (3, 100, cinema_id),
                    (4, 80, cinema_id),
                    (5, 80, cinema_id),
                    (6, 60, cinema_id)
                ]
                
                for screen in screens:
                    cursor.execute("""
                        INSERT INTO Screens (ScreenNumber, SeatCapacity, CinemaID)
                        SELECT ?, ?, ?
                        WHERE NOT EXISTS (
                            SELECT 1 FROM Screens 
                            WHERE ScreenNumber = ? AND CinemaID = ?
                        )
                    """, (screen[0], screen[1], screen[2], screen[0], screen[2]))

            self.connection.commit()
            print("Screens inserted successfully.")
            
        except Exception as e:
            print(f"Error inserting screens: {e}")
        finally:
            self.close()

    def initial_screenings(self):
        """Create screenings for each cinema's screens"""
        try:
            self.connect()
            cursor = self.connection.cursor()
            
            # Get all cinemas
            cursor.execute("SELECT CinemaID, CinemaName FROM Cinemas")
            cinemas = cursor.fetchall()
            
            # Template for screenings (film_id, screen_number, start_time, end_time)
            screening_templates = [
                # Screen 1 screenings
                (1, 1, "09:00", "11:00"),
                (2, 1, "13:30", "16:00"),
                (3, 1, "16:00", "18:00"),
                (5, 1, "18:00", "20:00"),
                (4, 1, "20:00", "22:00"),
                
                # Screen 2 screenings
                (1, 2, "11:00", "13:00"),
                (2, 2, "15:30", "18:00"),
                (3, 2, "18:00", "20:00"),
                (5, 2, "20:00", "22:00"),
                
                # Screen 3 screenings
                (4, 3, "09:00", "11:00"),
                (1, 3, "13:00", "15:00"),
                (3, 3, "20:00", "22:00"),
                
                # Screen 4 screenings
                (5, 4, "09:00", "11:00"),
                (4, 4, "11:00", "13:00"),
                (1, 4, "15:00", "17:00"),
                
                # Screen 5 screenings
                (3, 5, "09:00", "11:00"),
                (5, 5, "11:00", "13:00"),
                (4, 5, "13:00", "15:00"),
                
                # Screen 6 screenings
                (2, 6, "09:00", "11:30"),
                (3, 6, "11:30", "13:30"),
                (5, 6, "13:30", "15:30")
            ]

            # For each cinema, create screenings for its screens
            for cinema in cinemas:
                cinema_id = cinema['CinemaID']
                cinema_name = cinema['CinemaName']
                print(f"Creating screenings for {cinema_name}...")
                
                # For each screening template
                for film_id, screen_number, start_time, end_time in screening_templates:
                    # Find the actual screen ID for this cinema's screen number
                    cursor.execute(
                        "SELECT ScreenID, SeatCapacity FROM Screens WHERE ScreenNumber = ? AND CinemaID = ?", 
                        (screen_number, cinema_id)
                    )
                    screen_result = cursor.fetchone()
                    
                    if not screen_result:
                        print(f"Screen #{screen_number} not found for {cinema_name}, skipping.")
                        continue
                        
                    screen_id = screen_result['ScreenID']
                    total_seats = screen_result['SeatCapacity']
                    
                    # Calculate seat distributions
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
            print("Screenings created successfully for all cinemas.")
            
        except Exception as e:
            print(f"Error creating screenings: {e}")
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

    def insert_booking(self, user_id, customer_id, cinema_id, screening_id, booking_ref, total_price, cancellationfee, bookingdate, status):
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO Bookings (
                    UserID,
                    CustomerID,
                    CinemaID,
                    ScreeningID,
                    BookingReference,
                    TotalPrice,
                    BookingDate,
                    Status,
                    CancellationFee
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (customer_id, user_id, cinema_id, screening_id, booking_ref, total_price, bookingdate, status, cancellationfee))
            booking_id = cursor.lastrowid
            self.connection.commit()
        except Exception as e:
            print("Error inserting booking:", e)
            return []
        finally:
            self.close()
            return booking_id
    
    def get_booked_seat_counts(self, screening_id, booking_date, cinema_id):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT SeatType, COUNT(*) as Count
            FROM BookingSeats bs
            JOIN Bookings b ON b.BookingID = bs.BookingID
            WHERE b.ScreeningID = ? AND b.BookingDate = ? AND b.CinemaID = ? AND b.Status = 'active'
            GROUP BY SeatType
        """, (screening_id, booking_date, cinema_id))

        result = cursor.fetchall()
        return {row['SeatType']: row['Count'] for row in result}



    
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

    def get_customer_id_by_email(self, email):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT CustomreID FROM Customers WHERE Email = ?", (email,))
        row = cursor.fetchone()
        return row[0] if row else None

    def get_bookings_by_customer_id(self, user_id):
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
            WHERE b.UserID = ?
            GROUP BY b.BookingID
            ORDER BY b.BookingDate DESC
        """, (user_id,))
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_bookings_by_cinema_id(self, cinema_id):
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
            WHERE b.CinemaID = ?
            GROUP BY b.BookingID
            ORDER BY b.BookingDate DESC
        """, (cinema_id,))
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_all_bookings(self):
        return self.get_bookings(cinema_id=None, include_details=False)

    def get_bookings_by_cinema_id(self, cinema_id):
        return self.get_bookings(cinema_id=cinema_id, include_details=False)

    def get_bookings_with_email_cinema(self, cinema_id=None):
        return self.get_bookings(cinema_id=cinema_id, include_details=True)

    def get_all_bookings(self):
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
            GROUP BY b.BookingID
            ORDER BY b.BookingDate DESC
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_bookings(self, cinema_id=None, include_details=False):
        self.connect()
        cursor = self.connection.cursor()
        
        if include_details:
            base_query = """
                SELECT 
                    b.BookingReference,
                    f.Title,
                    b.BookingDate,
                    s.StartTime,
                    COUNT(bs.BookingSeatID) as SeatCount,
                    cu.Email as UserEmail,
                    c.CinemaName,
                    b.Status
                FROM Bookings b
                JOIN Screenings s ON b.ScreeningID = s.ScreeningID
                JOIN Films f ON s.FilmID = f.FilmID
                JOIN Customers cu ON b.CustomerID = cu.CustomerID
                JOIN Cinemas c ON b.CinemaID = c.CinemaID
                LEFT JOIN BookingSeats bs ON b.BookingID = bs.BookingID
            """
        else:
            base_query = """
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
            """
        
        if cinema_id is not None:
            filter_query = base_query + "WHERE b.CinemaID = ? GROUP BY b.BookingID ORDER BY b.BookingDate DESC"
            cursor.execute(filter_query, (cinema_id,))
        else:
            query = base_query + "GROUP BY b.BookingID ORDER BY b.BookingDate DESC"
            cursor.execute(query)
        
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
    
    def add_cinema_id_to_screens(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Check if CinemaID column exists
            cursor.execute("PRAGMA table_info(Screens)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if "CinemaID" not in columns:
                print("Adding CinemaID column to Screens table...")
                
                # Add the column
                cursor.execute("ALTER TABLE Screens ADD COLUMN CinemaID INTEGER")
                
                # Assign screens to cinemas evenly
                cursor.execute("SELECT CinemaID FROM Cinemas ORDER BY CinemaID")
                cinemas = cursor.fetchall()
                
                if cinemas:
                    # Get all screens
                    cursor.execute("SELECT ScreenID FROM Screens ORDER BY ScreenID")
                    screens = cursor.fetchall()
                    
                    # Distribute screens among cinemas
                    for i, screen in enumerate(screens):
                        cinema_id = cinemas[i % len(cinemas)]['CinemaID']
                        cursor.execute("UPDATE Screens SET CinemaID = ? WHERE ScreenID = ?", 
                                    (cinema_id, screen['ScreenID']))
                
                conn.commit()
                print("Migration completed successfully")
            else:
                print("CinemaID column already exists")
                
        except Exception as e:
            print(f"Migration error: {e}")
            if conn:
                conn.rollback()
        finally:

            self.close()

    def get_user_by_username(self, username):
        """Fetch user information by username"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE Username = ?", (username,))
        user = cursor.fetchone()

        self.close()
        return user
    






