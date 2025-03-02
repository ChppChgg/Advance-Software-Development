-- Table for Cinemas
CREATE TABLE Cinemas (
  cinema_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  city VARCHAR(100) NOT NULL,
  address VARCHAR(255)
);

-- Table for Screens
CREATE TABLE Screens (
  screen_id INT AUTO_INCREMENT PRIMARY KEY,
  cinema_id INT,
  screen_number INT NOT NULL,
  capacity INT NOT NULL,
  lower_hall_capacity INT,  -- Optional: store lower hall seat count
  FOREIGN KEY (cinema_id) REFERENCES Cinemas(cinema_id)
);

-- Table for Films
CREATE TABLE Films (
  film_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  genre VARCHAR(100),
  rating VARCHAR(10)
);

-- Table for Shows
CREATE TABLE Shows (
  show_id INT AUTO_INCREMENT PRIMARY KEY,
  film_id INT,
  screen_id INT,
  show_date DATE NOT NULL,
  show_time TIME NOT NULL,
  base_price DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (film_id) REFERENCES Films(film_id),
  FOREIGN KEY (screen_id) REFERENCES Screens(screen_id)
);

-- Table for Users
CREATE TABLE Users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('booking_staff', 'admin', 'manager') NOT NULL
);

-- Table for Bookings
CREATE TABLE Bookings (
  booking_id INT AUTO_INCREMENT PRIMARY KEY,
  show_id INT,
  user_id INT,
  booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  number_of_tickets INT NOT NULL,
  total_price DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (show_id) REFERENCES Shows(show_id),
  FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
