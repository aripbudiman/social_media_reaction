import tkinter as tk
from tkinter import messagebox


class ConfigWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Database Configuration")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Create form
        self.create_widgets()
        
    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.window, text="Database Configuration", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=20)
        
        # Frame for form
        form_frame = tk.Frame(self.window)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Host
        tk.Label(form_frame, text="Host:", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        self.host_entry = tk.Entry(form_frame, width=30)
        self.host_entry.grid(row=0, column=1, pady=5, padx=10)
        self.host_entry.insert(0, "localhost")
        
        # Username
        tk.Label(form_frame, text="Username:", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(form_frame, width=30)
        self.username_entry.grid(row=1, column=1, pady=5, padx=10)
        self.username_entry.insert(0, "root")
        
        # Password
        tk.Label(form_frame, text="Password:", anchor="w").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(form_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5, padx=10)
        
        # Database
        tk.Label(form_frame, text="Database:", anchor="w").grid(row=3, column=0, sticky="w", pady=5)
        self.database_entry = tk.Entry(form_frame, width=30)
        self.database_entry.grid(row=3, column=1, pady=5, padx=10)
        
        # Buttons frame
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)
        
        # Save button
        save_btn = tk.Button(button_frame, text="Save", width=10, 
                            command=self.save_config, bg="#4CAF50", fg="white")
        save_btn.grid(row=0, column=0, padx=5)
        
        # Test Connection button
        test_btn = tk.Button(button_frame, text="Test Connection", width=15, 
                            command=self.test_connection)
        test_btn.grid(row=0, column=1, padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", width=10, 
                              command=self.window.destroy)
        cancel_btn.grid(row=0, column=2, padx=5)
        
    def save_config(self):
        host = self.host_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        database = self.database_entry.get()
        
        if not all([host, username, database]):
            messagebox.showwarning("Warning", "Please fill in all required fields!")
            return
            
        # Simpan konfigurasi (bisa ke file atau variable)
        config = {
            'host': host,
            'username': username,
            'password': password,
            'database': database
        }
        
        messagebox.showinfo("Success", "Configuration saved successfully!")
        self.window.destroy()
        
    def test_connection(self):
        host = self.host_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        database = self.database_entry.get()
        
        if not all([host, username, database]):
            messagebox.showwarning("Warning", "Please fill in all fields to test connection!")
            return
            
        # Tambahkan logika test koneksi database di sini
        messagebox.showinfo("Test Connection", "Connection test would happen here!")

# # Update menu configuration Anda
# def open_settings():
#     ConfigWindow(root)

# config_menu = tk.Menu(menubar, tearoff=0)
# config_menu.add_command(label="Settings", command=open_settings)
# menubar.add_cascade(label="Configuration", menu=config_menu)