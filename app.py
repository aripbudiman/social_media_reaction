import tkinter as tk
from menubar import Menubar
from scrapping_youtube import YoutubeScraperApp

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Social Media Reaction")
    window.geometry("900x900")

    menubar = Menubar(window)
    menuScrapper= YoutubeScraperApp(window)

    window.mainloop()