import tkinter as tk
from tkinter import messagebox, filedialog
from config_window import ConfigWindow


class Menubar:
    def __init__(self, root):
        self.root = root

        # === MENU BAR / NAVBAR ===
        menubar = tk.Menu(root)

        # Menu FILE
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self._new_file)
        file_menu.add_command(label="Open...", command=self._open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._exit_app)
        menubar.add_cascade(label="File", menu=file_menu)

        # Menu EDIT
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo")
        edit_menu.add_command(label="Redo")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Menu HELP
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(
            label="About",
            command=lambda: messagebox.showinfo("About", "URILLL Universe App")
        )
        menubar.add_cascade(label="Help", menu=help_menu)

        # Menu Configuration
        config_menu = tk.Menu(menubar, tearoff=0)
        config_menu.add_command(label="Settings", command=self.open_settings)
        menubar.add_cascade(label="Configuration", menu=config_menu)

        # Pasang menu bar ke window
        root.config(menu=menubar)

    def _new_file(self):
        messagebox.showinfo("New File", "Menu New File diklik")

    def _open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            messagebox.showinfo("Open File", f"File dipilih:\n{file_path}")

    def _exit_app(self):
        self.root.quit()

    def open_settings(self):
        ConfigWindow(self.root)