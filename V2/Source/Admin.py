"""
Admin page functions
"""
import tkinter as tk
from tkinter import ttk, messagebox
from Basepage import BasePage

#Harry Elson, 23021935
#Matt Nogodula, 23015215
#Jerry Lin, 23024553

class AdminPage(BasePage):
    """Admin page for system management"""
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        
        # Content area
        content = tk.Frame(self.content_frame, bg="white")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Page title
        page_title = tk.Label(
            content,
            text="Admin Dashboard",
            font=("Arial", 16, "bold"),
            bg="white"
        )
        page_title.pack(anchor="w", pady=(0, 20))
        
        # Tabs for different admin functions
        tab_control = ttk.Notebook(content)
        
        # Films tab
        films_tab = ttk.Frame(tab_control)
        tab_control.add(films_tab, text="Films Management")
        
        # Screenings tab
        screenings_tab = ttk.Frame(tab_control)
        tab_control.add(screenings_tab, text="Screenings")
        
        # Reports tab
        reports_tab = ttk.Frame(tab_control)
        tab_control.add(reports_tab, text="Reports")
        
        # Users tab
        users_tab = ttk.Frame(tab_control)
        tab_control.add(users_tab, text="Users")

        staff_tab = ttk.Frame(tab_control)
        tab_control.add(staff_tab, text="Staff")
        
        tab_control.pack(expand=1, fill="both")
        
        # Films tab content
        self.setup_films_tab(films_tab)
        
        # Screenings tab content
        self.setup_screenings_tab(screenings_tab)
        
        # Reports tab content
        self.setup_reports_tab(reports_tab)
        
        # Users tab content
        self.setup_users_tab(users_tab)

        self.setup_staff_tab(staff_tab)
    
    def setup_films_tab(self, parent):
        """Set up the films management tab"""
        # Films list frame
        list_frame = tk.Frame(parent)
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Films treeview
        columns = ("id", "title", "genre", "duration", "rating")
        self.films_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        self.films_tree.heading("id", text="ID")
        self.films_tree.heading("title", text="Title")
        self.films_tree.heading("genre", text="Genre")
        self.films_tree.heading("duration", text="Duration")
        self.films_tree.heading("rating", text="Rating")
        
        # Define column widths
        self.films_tree.column("id", width=50)
        self.films_tree.column("title", width=200)
        self.films_tree.column("genre", width=100)
        self.films_tree.column("duration", width=80)
        self.films_tree.column("rating", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.films_tree.yview)
        self.films_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        scrollbar.pack(side="right", fill="y")
        self.films_tree.pack(fill="both", expand=True)
        
        # Films control frame
        control_frame = tk.Frame(parent)
        control_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        # Add film button
        add_button = tk.Button(
            control_frame,
            text="Add Film",
            width=15,
            command=lambda: messagebox.showinfo("Add Film", "Will be implemented later")
        )
        add_button.pack(pady=5)
        
        # Edit film button
        edit_button = tk.Button(
            control_frame,
            text="Edit Film",
            width=15,
            command=lambda: messagebox.showinfo("Edit Film", "Will be implemented later")
        )
        edit_button.pack(pady=5)
        
        # Delete film button
        delete_button = tk.Button(
            control_frame,
            text="Delete Film",
            width=15,
            command=lambda: messagebox.showinfo("Delete Film", "Will be implemented later")
        )
        delete_button.pack(pady=5)
    
    def setup_screenings_tab(self, parent):
        """Set up the screenings management tab"""
        label = tk.Label(parent, text="Screenings management will be implemented later")
        label.pack(pady=100)
    
    def setup_reports_tab(self, parent):
        """Set up the reports tab"""
        label = tk.Label(parent, text="Reports functionality will be implemented later")
        label.pack(pady=100)
    
    def setup_users_tab(self, parent):
        """Set up the users management tab"""
        label = tk.Label(parent, text="User management will be implemented later")
        label.pack(pady=100)

    def setup_staff_tab(self, parent):
        """Set up the staff management tab"""
        label = tk.Label(parent, text="User management will be implemented later")
        label.pack(pady=100)