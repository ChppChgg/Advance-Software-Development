import tkinter as tk
from tkinter import messagebox
from BasePage import BasePage

class SignupPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller)
        
        # Signup form
        signup_frame = tk.Frame(self.content, bg="white", padx=30, pady=30)
        signup_frame.place(relx=0.5, rely=0.4, anchor="center")
        signup_title = tk.Label(signup_frame, text="Sign Up", font=("Helvetica", 24), bg="white")
        signup_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        username_label = tk.Label(signup_frame, text="Username:", bg="white")
        username_label.grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(signup_frame, width=25)
        self.username_entry.grid(row=1, column=1, pady=5)
        password_label = tk.Label(signup_frame, text="Password:", bg="white")
        password_label.grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(signup_frame, width=25, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        confirm_password_label = tk.Label(signup_frame, text="Confirm Password:", bg="white")
        confirm_password_label.grid(row=3, column=0, sticky="w", pady=5)
        self.confirm_password_entry = tk.Entry(signup_frame, width=25, show="*")
        self.confirm_password_entry.grid(row=3, column=1, pady=5)
        signup_button = tk.Button(signup_frame, text="Sign Up", command=self.signup, 
                                bg="#ff4500", fg="white", width=10)
        signup_button.grid(row=4, column=1, sticky="e", pady=20)
        login_text = tk.Label(signup_frame, text="Already have an account?", bg="white")
        login_text.grid(row=5, column=0, sticky="w")
        login_link = tk.Label(signup_frame, text="Login", fg="blue", cursor="hand2", bg="white")
        login_link.grid(row=5, column=1, sticky="w")
        login_link.bind("<Button-1>", lambda e: controller.show_frame("LoginPage"))
    
    def signup(self):
        """Handle signup attempt"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        
        # In a real app, save user to database
        # Here we just show success message and redirect to login
        messagebox.showinfo("Success", "Account created successfully! Please log in.")
        
        # Clear fields
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)
        
        # Redirect to login page
        self.controller.show_frame("LoginPage")