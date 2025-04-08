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
                CinemaID INTEGER NOT NULL,
                ScreenNumber INTEGER NOT NULL,
                SeatCapacity INTEGER NOT NULL CHECK(SeatCapacity BETWEEN 50 AND 120),
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
                Date DATE NOT NULL,
                StartTime TIME NOT NULL,
                EndTime TIME NOT NULL,
                BasePrice REAL NOT NULL,
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
                ScreeningID INTEGER NOT NULL,
                BookingReference TEXT NOT NULL UNIQUE,
                TotalPrice REAL NOT NULL,
                BookingDateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                Status TEXT DEFAULT 'active' CHECK(Status IN ('active', 'cancelled')),
                CancellationFee REAL DEFAULT 0,
                FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE,
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
