import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os

class TabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tab Navigation Example")
        self.root.geometry("900x600")
        
        # Header
        header = tk.Frame(root, bg="#2C3E50", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="📊 Dashboard", 
                font=("Arial", 18, "bold"), 
                bg="#2C3E50", fg="white").pack(side="left", padx=20, pady=15)
        
        # Tab Navigation
        tab_frame = tk.Frame(root, bg="#34495E", height=50)
        tab_frame.pack(fill="x")
        tab_frame.pack_propagate(False)
        
        self.current_tab = "logs"
        
        # Tab Buttons
        self.logs_btn = tk.Button(tab_frame, text="📝 Logs", 
                                  font=("Arial", 11, "bold"),
                                  bg="#3498DB", fg="white",
                                  cursor="hand2",
                                  command=lambda: self.switch_tab("logs"),
                                  relief="flat",
                                  padx=20, pady=10)
        self.logs_btn.pack(side="left", padx=(20, 5), pady=10)
        
        self.explorer_btn = tk.Button(tab_frame, text="📁 Explorer", 
                                      font=("Arial", 11, "bold"),
                                      bg="#34495E", fg="white",
                                      cursor="hand2",
                                      command=lambda: self.switch_tab("explorer"),
                                      relief="flat",
                                      padx=20, pady=10)
        self.explorer_btn.pack(side="left", padx=5, pady=10)
        
        # Main Content Area
        self.content_frame = tk.Frame(root, bg="white")
        self.content_frame.pack(fill="both", expand=True)
        
        # Create both tabs
        self.create_logs_tab()
        self.create_explorer_tab()
        
        # Show logs tab by default
        self.switch_tab("logs")
    
    def switch_tab(self, tab_name):
        self.current_tab = tab_name
        
        # Update button styles
        if tab_name == "logs":
            self.logs_btn.config(bg="#3498DB")
            self.explorer_btn.config(bg="#34495E")
            self.logs_frame.pack(fill="both", expand=True)
            self.explorer_frame.pack_forget()
        else:
            self.logs_btn.config(bg="#34495E")
            self.explorer_btn.config(bg="#3498DB")
            self.explorer_frame.pack(fill="both", expand=True)
            self.logs_frame.pack_forget()
    
    def create_logs_tab(self):
        # Logs Tab - Single frame with log content
        self.logs_frame = tk.Frame(self.content_frame, bg="white")
        
        # Logs Header
        logs_header = tk.Frame(self.logs_frame, bg="#ECF0F1", height=50)
        logs_header.pack(fill="x")
        logs_header.pack_propagate(False)
        
        tk.Label(logs_header, text="System Logs", 
                font=("Arial", 13, "bold"), 
                bg="#ECF0F1").pack(side="left", padx=20, pady=10)
        
        clear_btn = tk.Button(logs_header, text="🗑 Clear Logs", 
                             font=("Arial", 9),
                             bg="#E74C3C", fg="white",
                             cursor="hand2",
                             command=self.clear_logs,
                             relief="flat",
                             padx=15, pady=5)
        clear_btn.pack(side="right", padx=20, pady=10)
        
        # Logs Content
        logs_container = tk.Frame(self.logs_frame, bg="white")
        logs_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(logs_container)
        scrollbar.pack(side="right", fill="y")
        
        # Text widget for logs
        self.logs_text = tk.Text(logs_container, 
                                font=("Consolas", 10),
                                bg="#1E1E1E", fg="#D4D4D4",
                                yscrollcommand=scrollbar.set,
                                relief="solid", bd=1,
                                wrap="word")
        self.logs_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.logs_text.yview)
        
        # Add sample logs
        self.add_log("INFO", "Application started")
        self.add_log("SUCCESS", "Connected to database")
        self.add_log("WARNING", "High memory usage detected")
        self.add_log("ERROR", "Failed to load configuration file")
        self.add_log("INFO", "User logged in successfully")
    
    def create_explorer_tab(self):
        # Explorer Tab - Split layout with sidebar and content
        self.explorer_frame = tk.Frame(self.content_frame, bg="white")
        
        # Explorer Header
        explorer_header = tk.Frame(self.explorer_frame, bg="#ECF0F1", height=50)
        explorer_header.pack(fill="x")
        explorer_header.pack_propagate(False)
        
        tk.Label(explorer_header, text="File Explorer", 
                font=("Arial", 13, "bold"), 
                bg="#ECF0F1").pack(side="left", padx=20, pady=10)
        
        # Main Explorer Container (sidebar + content)
        explorer_container = tk.Frame(self.explorer_frame, bg="white")
        explorer_container.pack(fill="both", expand=True)
        
        # LEFT SIDEBAR - Folder List
        sidebar = tk.Frame(explorer_container, bg="#F8F9FA", width=250, relief="solid", bd=1)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Sidebar Header
        sidebar_header = tk.Frame(sidebar, bg="#34495E", height=40)
        sidebar_header.pack(fill="x")
        sidebar_header.pack_propagate(False)
        
        tk.Label(sidebar_header, text="📂 Folders", 
                font=("Arial", 11, "bold"), 
                bg="#34495E", fg="white").pack(side="left", padx=15, pady=10)
        
        # Folder List
        folder_container = tk.Frame(sidebar, bg="#F8F9FA")
        folder_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        folder_scrollbar = tk.Scrollbar(folder_container)
        folder_scrollbar.pack(side="right", fill="y")
        
        self.folder_listbox = tk.Listbox(folder_container,
                                         font=("Arial", 10),
                                         bg="#F8F9FA",
                                         relief="flat",
                                         selectmode=tk.SINGLE,
                                         yscrollcommand=folder_scrollbar.set,
                                         activestyle="none")
        self.folder_listbox.pack(side="left", fill="both", expand=True)
        folder_scrollbar.config(command=self.folder_listbox.yview)
        self.folder_listbox.bind("<<ListboxSelect>>", self.on_folder_select)
        
        # RIGHT CONTENT - File List
        content_area = tk.Frame(explorer_container, bg="white")
        content_area.pack(side="right", fill="both", expand=True)
        
        # Content Header
        content_header = tk.Frame(content_area, bg="#ECF0F1", height=40)
        content_header.pack(fill="x")
        content_header.pack_propagate(False)
        
        self.content_title = tk.Label(content_header, text="📄 Files", 
                                      font=("Arial", 11, "bold"), 
                                      bg="#ECF0F1")
        self.content_title.pack(side="left", padx=20, pady=10)
        
        # File List with scrollbar
        file_container = tk.Frame(content_area, bg="white")
        file_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        file_scrollbar = tk.Scrollbar(file_container)
        file_scrollbar.pack(side="right", fill="y")
        
        self.file_listbox = tk.Listbox(file_container,
                                       font=("Consolas", 10),
                                       bg="white",
                                       relief="solid",
                                       bd=1,
                                       selectmode=tk.SINGLE,
                                       yscrollcommand=file_scrollbar.set,
                                       activestyle="none")
        self.file_listbox.pack(side="left", fill="both", expand=True)
        file_scrollbar.config(command=self.file_listbox.yview)
        
        # Initialize data folder and load folders
        self.data_folder = "data"  # Path ke folder data
        self.load_folders()
    
    def load_folders(self):
        """Load folders from data directory"""
        self.folder_listbox.delete(0, tk.END)
        
        # Check if data folder exists
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)  # Create if doesn't exist
            self.folder_listbox.insert(tk.END, "⚠️ Folder 'data' kosong")
            return
        
        # Read all folders in data directory
        try:
            items = os.listdir(self.data_folder)
            folders = [item for item in items if os.path.isdir(os.path.join(self.data_folder, item))]
            
            if folders:
                for folder in sorted(folders):
                    self.folder_listbox.insert(tk.END, f"📁 {folder}")
            else:
                self.folder_listbox.insert(tk.END, "⚠️ Tidak ada folder")
        except Exception as e:
            self.folder_listbox.insert(tk.END, f"❌ Error: {str(e)}")
    
    def on_folder_select(self, event):
        selection = self.folder_listbox.curselection()
        if selection:
            folder = self.folder_listbox.get(selection[0])
            # Remove emoji and get actual folder name
            folder_name = folder.replace("📁 ", "").replace("⚠️ ", "").replace("❌ ", "")
            
            # Skip if it's an error/warning message
            if folder_name in ["Folder 'data' kosong", "Tidak ada folder"] or "Error:" in folder_name:
                return
            
            self.load_files(folder_name)
    
    def load_files(self, folder_name):
        self.file_listbox.delete(0, tk.END)
        self.content_title.config(text=f"📄 Files in {folder_name}")
        
        # Real path to folder
        folder_path = os.path.join(self.data_folder, folder_name)
        
        if not os.path.exists(folder_path):
            self.file_listbox.insert(tk.END, "❌ Folder tidak ditemukan")
            return
        
        try:
            items = os.listdir(folder_path)
            files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
            
            if files:
                for file in sorted(files):
                    # Add icon based on extension
                    icon = self.get_file_icon(file)
                    self.file_listbox.insert(tk.END, f"{icon} {file}")
            else:
                self.file_listbox.insert(tk.END, "⚠️ Folder kosong")
        except Exception as e:
            self.file_listbox.insert(tk.END, f"❌ Error: {str(e)}")
    
    def get_file_icon(self, filename):
        """Return icon based on file extension"""
        ext = os.path.splitext(filename)[1].lower()
        
        icon_map = {
            '.txt': '📄',
            '.pdf': '📄',
            '.doc': '📄',
            '.docx': '📄',
            '.xls': '📊',
            '.xlsx': '📊',
            '.csv': '📊',
            '.ppt': '📊',
            '.pptx': '📊',
            '.jpg': '🖼',
            '.jpeg': '🖼',
            '.png': '🖼',
            '.gif': '🖼',
            '.mp4': '🎬',
            '.avi': '🎬',
            '.mov': '🎬',
            '.mp3': '🎵',
            '.wav': '🎵',
            '.zip': '📦',
            '.rar': '📦',
            '.py': '🐍',
            '.js': '📜',
            '.html': '🌐',
            '.css': '🎨',
        }
        
        return icon_map.get(ext, '📄')
    
    def add_log(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Color coding
        colors = {
            "INFO": "#3498DB",
            "SUCCESS": "#27AE60",
            "WARNING": "#F39C12",
            "ERROR": "#E74C3C"
        }
        
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)
        
        # Apply color tag
        line_start = self.logs_text.index("end-2c linestart")
        line_end = self.logs_text.index("end-1c")
        tag_name = f"tag_{level}"
        
        if tag_name not in self.logs_text.tag_names():
            self.logs_text.tag_config(tag_name, foreground=colors.get(level, "white"))
        
        self.logs_text.tag_add(tag_name, line_start, line_end)
    
    def clear_logs(self):
        self.logs_text.delete(1.0, tk.END)
        self.add_log("INFO", "Logs cleared")

if __name__ == "__main__":
    root = tk.Tk()
    app = TabApp(root)
    root.mainloop()