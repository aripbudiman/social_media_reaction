import tkinter as tk
from tkinter import messagebox, filedialog
from youtube import YoutubeScraper
from datetime import datetime 

class YoutubeScraperApp:
    def __init__(self, root):
        self.root = root
        
        # Header
        header = tk.Frame(root, bg="#FF0000", height=100)
        header.pack(fill="x")
        
        title = tk.Label(header, text="🎬 URILLL UNIVERSE", 
                        font=("Arial", 26, "bold"), 
                        bg="#FF0000", fg="white")
        title.pack(pady=25)


        # Input Frame
        input_frame = tk.Frame(root, bg="#f5f5f5", pady=20)
        input_frame.pack(fill="x")
        
        tk.Label(input_frame, text="YouTube URL:", 
                font=("Arial", 11, "bold"), 
                bg="#f5f5f5").pack(anchor="w", padx=25, pady=(0, 5))

        # URL Entry with example
        entry_container = tk.Frame(input_frame, bg="#f5f5f5")
        entry_container.pack(fill="x", padx=25)

        self.url_entry = tk.Entry(entry_container, font=("Arial", 11), 
                                    relief="solid", bd=1)
        self.url_entry.pack(fill="x", ipady=10,ipadx=20)
        self.url_entry.insert(0,"https://www.youtube.com/watch?v=...")
        self.url_entry.config(fg="gray")
        self.url_entry.bind("<FocusIn>", self._clear_placeholder)
        self.url_entry.bind("<FocusOut>", self._add_placeholder)
        self.url_entry.bind("<Return>", lambda e: self.start_scraping())

        # Example text
        tk.Label(input_frame, 
                text="Contoh: https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
                font=("Arial", 9), 
                bg="#f5f5f5", 
                fg="gray").pack(anchor="w", padx=25, pady=(3, 10))

        # Buttons
        btn_container = tk.Frame(input_frame, bg="#f5f5f5")
        btn_container.pack(fill="x", padx=25)

        self.scrape_btn = tk.Button(btn_container, 
                                    text="🚀 Mulai Scraping", 
                                    font=("Arial", 11, "bold"),
                                    bg="#FF0000", fg="white", 
                                    cursor="hand2",
                                    command=self._start_scraping, 
                                    relief="flat", 
                                    padx=20, pady=10)
        self.scrape_btn.pack(side="left", padx=(0, 10))

        clear_btn = tk.Button(btn_container, 
                            text="Clear Input", 
                            font=("Arial", 11, "bold"),
                            bg="#34495e", fg="white", 
                            cursor="hand2",
                            relief="flat",
                            padx=20, pady=10,
                            command=self._clear_input)
        clear_btn.pack(side="left")

        # Tab Navigation
        tab_frame = tk.Frame(root, height=30)
        tab_frame.pack(fill="x")
        tab_frame.pack_propagate(False)
        
        self.current_tab = "logs"
        
        # Tab Buttons
        self.logs_btn = tk.Button(tab_frame, text="📝 Logs", 
                                    font=("Arial", 9, "bold"),
                                    command=lambda: self.switch_tab("logs"),
                                    padx=20, pady=10)
        self.logs_btn.pack(side="left", padx=(0, 0), pady=0)
        
        self.explorer_btn = tk.Button(tab_frame, text="📁 Explorer", 
                                    font=("Arial", 9, "bold"),
                                    command=lambda: self.switch_tab("explorer"),
                                    padx=20, pady=10)
        self.explorer_btn.pack(side="left", padx=0, pady=0)

        # Main Content Area
        self.content_frame = tk.Frame(root, bg="#2c3e50")
        self.content_frame.pack(fill="both", expand=True)

        self.logs_frame = tk.Frame(self.content_frame, bg="#2c3e50")
        self.logs_frame.pack(fill="both", expand=True)


    def _clear_placeholder(self, event):
        if self.url_entry.get() == "https://www.youtube.com/watch?v=...":
            self.url_entry.delete(0, tk.END)
            self.url_entry.config(fg="black")
    
    def _add_placeholder(self, event):
        if not self.url_entry.get():
            self.url_entry.insert(0, "https://www.youtube.com/watch?v=...")
            self.url_entry.config(fg="gray")
    
    def _clear_input(self):
        self.url_entry.delete(0, tk.END)
        self.url_entry.config(fg="black")
        self.url_entry.focus()
    
    def _start_scraping(self):
        url = self.url_entry.get().strip()
        print(url)
        if not url or url == "https://www.youtube.com/watch?v=...":
            messagebox.showwarning("Peringatan", "Masukkan URL atau ID YouTube!")
            return
        # Disable button during scraping
        self.scrape_btn.config(state="disabled", text="⏳ Scraping...")
        
        scraper = YoutubeScraper(url)
        scraper.process()
        
        # Simulate scraping process
        self.root.after(1500, lambda: self.finish_scraping(url))

    def finish_scraping(self, url):
        # Extract video ID (simplified)
        video_id = url.split("v=")[-1].split("&")[0] if "v=" in url else url
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"youtube_{video_id[:11]}_{timestamp}.csv"
        
        # Reset button
        self.scrape_btn.config(state="normal", text="🚀 Mulai Scraping")
        
        # Clear input
        self.url_entry.delete(0, tk.END)
        
        # self.update_footer()
        
        messagebox.showinfo("Sukses", f"Scraping selesai!")
    