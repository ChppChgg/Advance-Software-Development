import sqlite3
import os 
db_path = os.path.abspath("HorizonHotelsT/Data/CinemaDatabase.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")
cursor.executescript('''
    CREATE TABLE IF NOT EXISTS Cinema (
        CinemaID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Location TEXT NOT NULL,
        NumberOfScreens INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Screen (
        ScreenID INTEGER PRIMARY KEY,
        CinemaID INTEGER NOT NULL,
        ScreenNumber INTEGER NOT NULL,
        SeatCapacity INTEGER NOT NULL,
        FOREIGN KEY (CinemaID) REFERENCES Cinema(CinemaID)
    );

    CREATE TABLE IF NOT EXISTS Film (
        FilmID INTEGER PRIMARY KEY,
        Title TEXT NOT NULL,
        Duration INTEGER NOT NULL,
        Genre TEXT NOT NULL,
        Rating TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Screening (
        ScreeningID INTEGER PRIMARY KEY,
        FilmID INTEGER NOT NULL,
        ScreenID INTEGER NOT NULL,
        StartTime TEXT NOT NULL,
        EndTime TEXT NOT NULL,
        Date TEXT NOT NULL,
        FOREIGN KEY (FilmID) REFERENCES Film(FilmID),
        FOREIGN KEY (ScreenID) REFERENCES Screen(ScreenID)
    );

    CREATE TABLE IF NOT EXISTS Customer (
        CustomerID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Email TEXT UNIQUE NOT NULL,
        PhoneNumber TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Booking (
        BookingID INTEGER PRIMARY KEY,
        CustomerID INTEGER NOT NULL,
        ScreeningID INTEGER NOT NULL,
        NumberOfSeats INTEGER NOT NULL,
        BookingDate TEXT NOT NULL,
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
        FOREIGN KEY (ScreeningID) REFERENCES Screening(ScreeningID)
    );

    CREATE TABLE IF NOT EXISTS Seat (
        SeatID INTEGER PRIMARY KEY,
        ScreenID INTEGER NOT NULL,
        SeatNumber TEXT NOT NULL,
        FOREIGN KEY (ScreenID) REFERENCES Screen(ScreenID)
    );

    CREATE TABLE IF NOT EXISTS Booking_Seat (
        BookingID INTEGER NOT NULL,
        SeatID INTEGER NOT NULL,
        PRIMARY KEY (BookingID, SeatID),
        FOREIGN KEY (BookingID) REFERENCES Booking(BookingID),
        FOREIGN KEY (SeatID) REFERENCES Seat(SeatID)
    );
''')

conn.commit()
conn.close()
