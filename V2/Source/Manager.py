"""
Manager page 
"""
import tkinter as tk
from tkinter import ttk, messagebox
from Basepage import BasePage

class ManagerPage(BasePage):
    """Manager page for cinema management"""
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        
        # Content area
        content = tk.Frame(self.content_frame, bg="white")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Page title
        page_title = tk.Label(
            content,
            text="Cinema Manager Dashboard",
            font=("Arial", 16, "bold"),
            bg="white"
        )
        page_title.pack(anchor="w", pady=(0, 20))
        
        # Tabs for different manager functions
        tab_control = ttk.Notebook(content)
        
        # Cinemas tab
        cinemas_tab = ttk.Frame(tab_control)
        tab_control.add(cinemas_tab, text="Cinemas")
        
        # Screens tab
        screens_tab = ttk.Frame(tab_control)
        tab_control.add(screens_tab, text="Screens")
        
        tab_control.pack(expand=1, fill="both")
        
        # Cinemas tab content
        self.setup_cinemas_tab(cinemas_tab)
        
        # Screens tab content
        self.setup_screens_tab(screens_tab)
    
    def setup_cinemas_tab(self, parent):
        """Set up the cinemas management tab"""
        # Cinemas list frame
        list_frame = tk.Frame(parent)
        list_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Cinemas treeview
        columns = ("id", "name", "city", "address", "screens")
        self.cinemas_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        self.cinemas_tree.heading("id", text="ID")
        self.cinemas_tree.heading("name", text="Name")
        self.cinemas_tree.heading("city", text="City")
        self.cinemas_tree.heading("address", text="Address")
        self.cinemas_tree.heading("screens", text="Screens")
        
        # Define column widths
        self.cinemas_tree.column("id", width=50)
        self.cinemas_tree.column("name", width=150)
        self.cinemas_tree.column("city", width=100)
        self.cinemas_tree.column("address", width=200)
        self.cinemas_tree.column("screens", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.cinemas_tree.yview)
        self.cinemas_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        scrollbar.pack(side="right", fill="y")
        self.cinemas_tree.pack(fill="both", expand=True)
        
        # Cinemas control frame
        control_frame = tk.Frame(parent)
        control_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        # Add cinema button
        add_button = tk.Button(
            control_frame,
            text="Add Cinema",
            width=15,
            command=lambda: messagebox.showinfo("Add Cinema", "Will be implemented later")
        )
        add_button.pack(pady=5)
        
        # Edit cinema button
        edit_button = tk.Button(
            control_frame,
            text="Edit Cinema",
            width=15,
            command=lambda: messagebox.showinfo("Edit Cinema", "Will be implemented later")
        )
        edit_button.pack(pady=5)
        
        # Delete cinema button
        delete_button = tk.Button(
            control_frame,
            text="Delete Cinema",
            width=15,
            command=lambda: messagebox.showinfo("Delete Cinema", "Will be implemented later")
        )
        delete_button.pack(pady=5)
    
    def setup_screens_tab(self, parent):
        """Set up the screens management tab"""
        label = tk.Label(parent, text="Screens management will be implemented later")
        label.pack(pady=100)