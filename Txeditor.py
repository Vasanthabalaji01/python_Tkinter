import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter import font as tkFont

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Txeditor")

        # Set custom icon
        icon_path = "assets/Mr.Cloudexplorer_logo.ico"
        self.root.iconbitmap(default=icon_path)

        # Get the default system font
        self.default_font = tkFont.nametofont("TkDefaultFont")

        self.text_widget = tk.Text(root, wrap="word", undo=True, font=self.default_font)
        self.text_widget.pack(expand="yes", fill="both")

        # Create a menu bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.destroy)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_widget.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_widget.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all)

        # Search menu
        self.search_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Search", menu=self.search_menu)
        self.search_menu.add_command(label="Find", command=self.find_text)

        # View menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Zoom In", command=self.zoom_in)
        self.view_menu.add_command(label="Zoom Out", command=self.zoom_out)

        # Status Bar
        self.status_bar = tk.Label(root, text="Ln 1, Col 1", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Zoom level
        self.zoom_level = 100

        # Event bindings
        self.text_widget.bind("<Key>", self.update_status_bar)
        self.text_widget.bind("<Button-1>", self.update_status_bar)
        self.text_widget.bind("<Enter>", self.update_status_bar)

    def new_file(self):
        self.text_widget.delete("1.0", tk.END)
        self.update_status_bar()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert(tk.END, content)
            self.root.title(f"Txeditor - {file_path}")
            self.update_status_bar()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_widget.get("1.0", tk.END)
                file.write(content)
            self.root.title(f"Txeditor - {file_path}")
            self.update_status_bar()

    def save_as_file(self):
        self.save_file()

    def cut(self):
        self.text_widget.event_generate("<<Cut>>")
        self.update_status_bar()

    def copy(self):
        self.text_widget.event_generate("<<Copy>>")
        self.update_status_bar()

    def paste(self):
        self.text_widget.event_generate("<<Paste>>")
        self.update_status_bar()

    def select_all(self):
        self.text_widget.tag_add(tk.SEL, "1.0", tk.END)
        self.update_status_bar()

    def find_text(self):
        find_string = simpledialog.askstring("Find", "Enter text to find:")
        if find_string:
            start_pos = "1.0"
            end_pos = tk.END
            count_var = tk.StringVar()
            count_var.set(self.text_widget.search(find_string, start_pos, stopindex=end_pos, count=count_var))
            if count_var.get():
                self.text_widget.tag_add(tk.SEL, count_var.get(), f"{count_var.get()}+{len(find_string)}c")
                self.text_widget.focus_set()

    def update_status_bar(self, event=None):
        cursor_position = self.text_widget.index(tk.CURRENT)
        line, col = cursor_position.split(".")
        status_text = f"Ln {line}, Col {col}"
        self.status_bar.config(text=status_text)

    def zoom_in(self):
        self.zoom_level += 10
        self.update_zoom()

    def zoom_out(self):
        self.zoom_level -= 10
        self.update_zoom()

    def update_zoom(self):
        new_font_size = int(self.default_font.actual()['size'] * (self.zoom_level / 100))
        self.text_widget.configure(font=(self.default_font.actual()['family'], new_font_size))

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.geometry("800x600")  # Set a default window size
    root.eval('tk::PlaceWindow . center')  # Center the window on the screen
    root.mainloop()
