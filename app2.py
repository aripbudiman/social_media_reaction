import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import os

class YouTubeScraperApp:
    def __init__(self, root):
        
        self.root = root
        self.root.title("🎬 URILLL UNIVERSE")
        self.root.geometry("900x900")
        self.root.resizable(False, False)
        
        # Data scraped files
        self.scraped_files = []
        self.is_scraping = False
        
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
        
        tk.Label(input_frame, text="YouTube URL atau Video ID:", 
                font=("Arial", 11, "bold"), 
                bg="#f5f5f5").pack(anchor="w", padx=25, pady=(0, 5))
        
        # URL Entry with example
        entry_container = tk.Frame(input_frame, bg="#f5f5f5")
        entry_container.pack(fill="x", padx=25)
        
        self.url_entry = tk.Entry(entry_container, font=("Arial", 11), 
                                    relief="solid", bd=1)
        self.url_entry.pack(fill="x", ipady=8)
        self.url_entry.insert(0, "https://www.youtube.com/watch?v=...")
        self.url_entry.config(fg="gray")
        self.url_entry.bind("<FocusIn>", self.clear_placeholder)
        self.url_entry.bind("<FocusOut>", self.add_placeholder)
        self.url_entry.bind("<Return>", lambda e: self.start_scraping())
        
        # Example text
        tk.Label(input_frame, 
                text="Contoh: https://www.youtube.com/watch?v=dQw4w9WgXcQ atau dQw4w9WgXcQ", 
                font=("Arial", 9), 
                bg="#f5f5f5", 
                fg="gray").pack(anchor="w", padx=25, pady=(3, 10))
        
        # Buttons
        btn_container = tk.Frame(input_frame, bg="#f5f5f5")
        btn_container.pack(fill="x", padx=25)
        
        self.scrape_btn = tk.Button(btn_container, text="🚀 Mulai Scraping", 
                                    font=("Arial", 11, "bold"),
                                    bg="#FF0000", fg="white", 
                                    cursor="hand2",
                                    command=self.start_scraping, 
                                    relief="flat", 
                                    padx=20, pady=10)
        self.scrape_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = tk.Button(btn_container, text="🗑 Clear Input", 
                            font=("Arial", 10),
                            bg="#757575", fg="white", 
                            cursor="hand2",
                            command=self.clear_input, 
                            relief="flat", 
                            padx=15, pady=10)
        clear_btn.pack(side="left")
        
        # Progress/Status Frame
        status_frame = tk.Frame(root, bg="white", pady=15)
        status_frame.pack(fill="x", padx=25, pady=(10, 0))
        
        self.status_label = tk.Label(status_frame, 
                                     text="Status: Menunggu input...", 
                                     font=("Arial", 10), 
                                     bg="white", 
                                     fg="#666",
                                     anchor="w")
        self.status_label.pack(fill="x", padx=10)
        
        # Progress bar placeholder
        self.progress_frame = tk.Frame(status_frame, bg="white", height=8)
        self.progress_frame.pack(fill="x", padx=10, pady=(5, 0))
        
        # Separator
        separator = tk.Frame(root, bg="#ddd", height=2)
        separator.pack(fill="x", padx=25, pady=15)
        
        # Files List Section
        files_header = tk.Frame(root, bg="white")
        files_header.pack(fill="x", padx=25)
        
        tk.Label(files_header, text="📁 File CSV Hasil Scraping", 
                font=("Arial", 13, "bold"), 
                bg="white").pack(side="left")
        
        export_btn = tk.Button(files_header, text="📤 Export All", 
                              font=("Arial", 9),
                              bg="#4CAF50", fg="white", 
                              cursor="hand2",
                              command=self.export_files, 
                              relief="flat", 
                              padx=10, pady=5)
        export_btn.pack(side="right")
        
        # Files List Frame
        list_frame = tk.Frame(root, bg="white")
        list_frame.pack(fill="both", expand=True, padx=25, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.files_listbox = tk.Listbox(list_frame, 
                                        font=("Consolas", 10),
                                        selectmode=tk.SINGLE, 
                                        yscrollcommand=scrollbar.set,
                                        relief="solid", 
                                        bd=1,
                                        activestyle="none",
                                        bg="#fafafa")
        self.files_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.files_listbox.yview)
        self.files_listbox.bind("<Double-Button-1>", self.open_file)
        
        # Action Buttons Frame
        action_frame = tk.Frame(root, bg="white")
        action_frame.pack(fill="x", padx=25, pady=10)
        
        open_btn = tk.Button(action_frame, text="📂 Buka File", 
                            font=("Arial", 9),
                            bg="#2196F3", fg="white",
                            cursor="hand2", 
                            command=self.open_selected_file,
                            relief="flat", 
                            padx=15, pady=5)
        open_btn.pack(side="left", padx=5)
        
        delete_btn = tk.Button(action_frame, text="🗑 Hapus", 
                              font=("Arial", 9),
                              bg="#f44336", fg="white",
                              cursor="hand2", 
                              command=self.delete_file,
                              relief="flat", 
                              padx=15, pady=5)
        delete_btn.pack(side="left", padx=5)
        
        clear_all_btn = tk.Button(action_frame, text="🧹 Hapus Semua", 
                                 font=("Arial", 9),
                                 bg="#FF9800", fg="white",
                                 cursor="hand2", 
                                 command=self.clear_all_files,
                                 relief="flat", 
                                 padx=15, pady=5)
        clear_all_btn.pack(side="right", padx=5)
        
        # Footer Status Bar
        footer = tk.Frame(root, bg="#f0f0f0", height=30)
        footer.pack(fill="x", side="bottom")
        
        self.footer_label = tk.Label(footer, 
                                     text="Total file: 0", 
                                     font=("Arial", 9), 
                                     bg="#f0f0f0", 
                                     anchor="w", 
                                     padx=15)
        self.footer_label.pack(fill="both", expand=True)
        
        self.update_footer()
    
    def clear_placeholder(self, event):
        if self.url_entry.get() == "https://www.youtube.com/watch?v=...":
            self.url_entry.delete(0, tk.END)
            self.url_entry.config(fg="black")
    
    def add_placeholder(self, event):
        if not self.url_entry.get():
            self.url_entry.insert(0, "https://www.youtube.com/watch?v=...")
            self.url_entry.config(fg="gray")
    
    def clear_input(self):
        self.url_entry.delete(0, tk.END)
        self.url_entry.config(fg="black")
        self.url_entry.focus()
    
    def start_scraping(self):
        url = self.url_entry.get().strip()
        
        if not url or url == "https://www.youtube.com/watch?v=...":
            messagebox.showwarning("Peringatan", "Masukkan URL atau ID YouTube!")
            return
        
        # Disable button during scraping
        self.scrape_btn.config(state="disabled", text="⏳ Scraping...")
        self.status_label.config(text="Status: Sedang scraping...", fg="#FF9800")
        
        # Simulate scraping process
        self.root.after(1500, lambda: self.finish_scraping(url))
    
    def finish_scraping(self, url):
        # Extract video ID (simplified)
        video_id = url.split("v=")[-1].split("&")[0] if "v=" in url else url
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"youtube_{video_id[:11]}_{timestamp}.csv"
        
        # Add to list
        self.scraped_files.append({
            "filename": filename,
            "url": url,
            "time": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%d/%m/%Y")
        })
        
        # Update listbox
        display_text = f"✅ {filename} - {self.scraped_files[-1]['time']}"
        self.files_listbox.insert(tk.END, display_text)
        self.files_listbox.itemconfig(tk.END, fg="#4CAF50")
        
        # Reset button
        self.scrape_btn.config(state="normal", text="🚀 Mulai Scraping")
        self.status_label.config(text="Status: Scraping selesai! ✓", fg="#4CAF50")
        
        # Clear input
        self.url_entry.delete(0, tk.END)
        
        self.update_footer()
        
        messagebox.showinfo("Sukses", f"Scraping selesai!\nFile: {filename}")
    
    def open_file(self, event):
        self.open_selected_file()
    
    def open_selected_file(self):
        try:
            index = self.files_listbox.curselection()[0]
            filename = self.scraped_files[index]["filename"]
            messagebox.showinfo("Info", f"Membuka file: {filename}\n\n(Fungsi buka file akan diimplementasikan)")
        except IndexError:
            messagebox.showwarning("Peringatan", "Pilih file terlebih dahulu!")
    
    def delete_file(self):
        try:
            index = self.files_listbox.curselection()[0]
            filename = self.scraped_files[index]["filename"]
            
            if messagebox.askyesno("Konfirmasi", f"Hapus file {filename}?"):
                self.files_listbox.delete(index)
                self.scraped_files.pop(index)
                self.update_footer()
                self.status_label.config(text=f"Status: File {filename} dihapus", fg="#f44336")
        except IndexError:
            messagebox.showwarning("Peringatan", "Pilih file terlebih dahulu!")
    
    def clear_all_files(self):
        if self.scraped_files:
            if messagebox.askyesno("Konfirmasi", "Hapus semua file?"):
                self.files_listbox.delete(0, tk.END)
                self.scraped_files.clear()
                self.update_footer()
                self.status_label.config(text="Status: Semua file dihapus", fg="#f44336")
        else:
            messagebox.showinfo("Info", "Tidak ada file untuk dihapus!")
    
    def export_files(self):
        if not self.scraped_files:
            messagebox.showinfo("Info", "Tidak ada file untuk di-export!")
            return
        
        folder = filedialog.askdirectory(title="Pilih Folder Tujuan Export")
        if folder:
            messagebox.showinfo("Sukses", f"Export {len(self.scraped_files)} file ke:\n{folder}")
    
    def update_footer(self):
        total = len(self.scraped_files)
        self.footer_label.config(text=f"Total file: {total}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeScraperApp(root)
    root.mainloop()