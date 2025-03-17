import tkinter as tk
from tkinter import messagebox
from BasePage import BasePage

class LoginPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        
        # Login form
        login_frame = tk.Frame(self.content, bg="white", padx=30, pady=30)
        login_frame.place(relx=0.5, rely=0.4, anchor="center")
        login_title = tk.Label(login_frame, text="Login", font=("Helvetica", 24), bg="white")
        login_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        username_label = tk.Label(login_frame, text="Username:", bg="white")
        username_label.grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(login_frame, width=25)
        self.username_entry.grid(row=1, column=1, pady=5)
        password_label = tk.Label(login_frame, text="Password:", bg="white")
        password_label.grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(login_frame, width=25, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        login_button = tk.Button(login_frame, text="Login", command=self.login, 
                               bg="#ff4500", fg="white", width=10)
        login_button.grid(row=3, column=1, sticky="e", pady=20)
        signup_text = tk.Label(login_frame, text="Don't have an account?", bg="white")
        signup_text.grid(row=4, column=0, sticky="w")
        signup_link = tk.Label(login_frame, text="Sign up", fg="blue", cursor="hand2", bg="white")
        signup_link.grid(row=4, column=1, sticky="w")
        signup_link.bind("<Button-1>", lambda e: controller.show_frame("SignupPage"))
    
    def login(self):
        """Handle login attempt"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return
        
        # In a real app, validate against database
        # For now, accept any non-empty credentials
        self.controller.login_user(username)
        
        # Update sidebar to show logout button
        self.update_sidebar()
        
        messagebox.showinfo("Success", f"Welcome, {username}!")
    
    def on_show(self):
        """Reset fields when page is shown"""
        # Clear password field for security
        self.password_entry.delete(0, tk.END)