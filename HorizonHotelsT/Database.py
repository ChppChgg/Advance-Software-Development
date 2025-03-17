import sqlite3
import os 
db_path = os.path.abspath("HorizonHotelsT/Data/CinemaDatabase.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")
cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               Username TEXT NOT NULL,
               Password TEXT NOT NULL,
               userType INT
               );

        CREATE TABLE IF NOT EXISTS Cinema (
               cinema INT NOT NULL,
               Location TEXT NOT NULL,
               Screens INT NOT NULL
               );
        
        /* CREATE TABLE IF NOT EXISTS Screen (
               FOREIGN KEY(cinema) REFERENCES Cinema(cinema) ON DELETE CASCADE,
               Shows TEXT NOT NULL,
               Capacity INT
               );
       
            CREATE TABLE IF NOT EXISTS Screening (
                )
            
            CREATE TABLE IF NOT EXISTS Seat (
                seatNumber PRIMARY KEY,
                seatType TEXT NOT NULL,
                isBooked BOOLEAN NOT NULL
                )
        */
                      
                     
        CREATE TABLE IF NOT EXISTS Booking (
                bookingID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT,
                FOREIGN KEY (Username) REFERENCES users(Username) ON DELETE CASCADE
                );
        
''')
conn.commit()
conn.close()
