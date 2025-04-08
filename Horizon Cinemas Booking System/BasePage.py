import tkinter as tk

class BasePage(tk.Frame):
    """Base class for all pages with common elements"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ffffff")
        self.controller = controller
        
        # Create header
        self.header = tk.Frame(self, bg="#000000", height=60)
        self.header.pack(fill="x", side="top")
        
        # Logo in header
        logo_label = tk.Label(self.header, text="Horizon Movies", font=("Helvetica", 24, "bold"), 
                             bg="#000000", fg="#ff4500")
        logo_label.pack(side="left", padx=20)
        
        # Create sidebar
        self.sidebar = tk.Frame(self, bg="#111111", width=250)
        self.sidebar.pack(fill="y", side="left")
        self.sidebar.pack_propagate(False)  # Prevent the sidebar from shrinking
        
        # Create content area
        self.content = tk.Frame(self, bg="#ffffff")
        self.content.pack(fill="both", expand=True)
        
        # Add sidebar navigation
        self.create_sidebar_nav()
    
    def create_sidebar_nav(self):
        """Create navigation links in sidebar"""
        # Search box at the top
        search_frame = tk.Frame(self.sidebar, bg="#111111", pady=20)
        search_frame.pack(fill="x")
        
        search_entry = tk.Entry(search_frame, bg="#333333", fg="white", 
                               insertbackground="white")
        search_entry.pack(fill="x", padx=20)
        
        # Navigation buttons
        nav_buttons = [
            {"text": "Home", "command": lambda: self.controller.show_frame("HomePage")},
            {"text": "Book Tickets", "command": lambda: self.controller.show_frame("BookingPage")},
        ]
        
        for btn in nav_buttons:
            button = tk.Button(self.sidebar, text=btn["text"], command=btn["command"],
                              bg="#111111", fg="white", bd=0, font=("Helvetica", 12),
                              activebackground="#ff4500", activeforeground="white",
                              width=20, anchor="w", padx=20, pady=10)
            button.pack(fill="x")
        
        # Create logout button (will be shown/hidden based on login status)
        self.logout_button = tk.Button(self.sidebar, text="Logout", 
                                     command=self.controller.logout_user,
                                     bg="#111111", fg="white", bd=0, 
                                     activebackground="#ff4500", font=("Helvetica", 12),
                                     width=20, anchor="w", padx=20, pady=10)
        
        # Update sidebar based on current login status
        self.update_sidebar()
    
    def update_sidebar(self):
        """Update sidebar elements based on login status"""
        if hasattr(self.controller, 'current_user') and self.controller.current_user:
            # User is logged in, show logout button
            self.logout_button.pack(fill="x", side="bottom")
        else:
            # User is not logged in, hide logout button
            self.logout_button.pack_forget()
