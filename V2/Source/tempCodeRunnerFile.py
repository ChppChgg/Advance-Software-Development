def insert_initial_films(self):
        """Insert predefined films into the Films table if they don't already exist."""
        films_to_add = [
            ("A Minecraft Movie", "Four misfits are suddenly pulled through a mysterious portal into a bizarre cubic wonderland that thrives on imagination. To get back home they'll have to master this world while embarking on a quest with an unexpected expert crafter.", "Jack Black, Jason Mamoa, Sebastian Hansen", "Comedy", "PG", 101),
            ("The Amateur", "When a CIA cryptographer discovers that terrorists were behind his fiancée's death in a suspicious plane crash, he receives special training in order to plot his revenge.", "Rami Malek, Rachel Brosnahan, Caitriona Balfe, Julianne Nicholson, Holt McCallany", "Spy", "12A", 122),
            ("DROP", "First dates are nerve-wracking enough. Going on a first date while an unnamed unseen troll pings you personal memes that escalate from annoying to homicidal?", "Meghann Fahy, Brandon Sklenar, Violett Beane, Jacob Robinson, Ed Weeks, Jeffery Self", "Thriller", "15", 95),
            ("Death of a Unicorn", "Father-Daughter duo, Riley and Elliot, hit a unicorn with their car and bring it to the wilderness retreat of a mega-wealthy pharmaceutical CEO.", "Paul Rudd, Jenna Ortega, Téa Leoni, Will Poulter, Richard E Grant", "Comedy / Horror", "15", 107),
            ("Until Dawn", "One year after her sister Melanie mysteriously disappeared, Clover and her friends head into the remote valley where she vanished in search of answers.", "Ella Rubin, Michael Cimino, Odessa Azion, Ji-young Yoo, Belmont Cameli, Maia Mitchell, Peter Stormare", "Adventure", "15", 103),
            ("Star Wars: Episode III - Revenge of the Sith (20th anniversary)", "Three years into the Clone Wars, the Jedi rescue Palpatine from Count Dooku. As Obi-Wan pursues a new threat, Anakin acts as a double agent...", "Christopher Lee, Natalie Portman, Hayden Christensen, Ian McDiarmid, Frank Oz, Ewan McGregor, Samuel L. Jackson, Anthony Daniels, Kenny Baker", "Sci-Fi", "12A", 140),
            ("The Last Journey", "Follow Filip Hammar as he takes his dad on a road trip through Europe, down to the Mediterranean, with his best mate Fredrik Wikingsson.", "Filip Hammar, Fredrik Wikingsson, Lars Hammar, Tiina Hammar", "Documentary", "PG", 95),
            ("A Working Man", "Levon Cade left his profession behind to work construction and be a good dad to his daughter. But when a local girl vanishes, he's asked to return.", "Jason Statham, Jason Flemyng, Merab Ninidze, Maximilian Osinski, Cokey Falkow, Michael Pena, David Harbour, Noemi Gonzalez, Arianna Rivas, Emmett J Scanlan, Eve Mauro", "Action / Thriller", "15", 116)
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