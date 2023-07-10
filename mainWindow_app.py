import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import patoolib
import shutil
from web_site_surf import browse_into_web


class ImageAlbum:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.current_image_index = 0
        self.theme = "light"
        self.browser_frame = None
        self.prev_button = None
        self.next_button = None

        # Create a menu bar
        menu_bar = tk.Menu(root)

        # Create File menu and add it to the menu bar
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Create Convert menu and add it to the menu bar
        convert_menu = tk.Menu(menu_bar, tearoff=0)
        convert_menu.add_command(label="Convert", command=self.convert)
        menu_bar.add_cascade(label="Convert", menu=convert_menu)

        # Create Toggle menu and add it to the menu bar
        toggle_menu = tk.Menu(menu_bar, tearoff=0)
        toggle_menu.add_command(label="Toggle", command=self.toggle)
        menu_bar.add_cascade(label="Toggle", menu=toggle_menu)

        # Create Web menu and add it to the menu bar
        web_menu = tk.Menu(menu_bar, tearoff=0)
        web_menu.add_command(label="Web", command=self.web)
        menu_bar.add_cascade(label="Web", menu=web_menu)

        # Create Trends menu and add it to the menu bar
        trends_menu = tk.Menu(menu_bar, tearoff=0)
        trends_menu.add_command(label="Trends", command=self.trends)
        menu_bar.add_cascade(label="Trends", menu=trends_menu)

        # Create To-do menu and add it to the menu bar
        todo_menu = tk.Menu(menu_bar, tearoff=0)
        todo_menu.add_command(label="To-do", command=self.todo)
        menu_bar.add_cascade(label="To-do", menu=todo_menu)

        # Create Database menu and add it to the menu bar
        db_menu = tk.Menu(menu_bar, tearoff=0)
        db_menu.add_command(label="Insert", command=self.insert_into_db)
        db_menu.add_command(label="Open", command=self.open_from_db)
        menu_bar.add_cascade(label="Database", menu=db_menu)

        # Create Screen mode menu and add it to the menu bar
        screen_mode_menu = tk.Menu(menu_bar, tearoff=0)
        screen_mode_menu.add_command(label="Fullscreen", command=self.toggle_fullscreen)
        menu_bar.add_cascade(label="Screen mode", menu=screen_mode_menu)

        root.config(menu=menu_bar)

        # Create a label to display the image
        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.set_theme()

    def open_file(self):
        filetypes = (
            ("Comic Book Archives", "*.cbr *.cbz *.cbt *.cba *.cb7"),
            ("All Files", "*.*")
        )
        filepath = filedialog.askopenfilename(filetypes=filetypes)

        if filepath:
            # Extract the contents of the selected file to a temporary directory
            temp_dir = "_temp"
            os.makedirs(temp_dir, exist_ok=True)
            patoolib.extract_archive(filepath, outdir=temp_dir, interactive=False)

            # Get the paths of the extracted images
            self.image_paths = []
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        self.image_paths.append(os.path.join(root, file))

            # Display the first image and show navigation buttons
            if self.image_paths:
                self.current_image_index = 0
                self.show_image(self.image_paths[self.current_image_index])

                self.prev_button = tk.Button(self.root, text="Previous", command=self.show_previous_image)
                self.next_button = tk.Button(self.root, text="Next", command=self.show_next_image)

                self.prev_button.pack(side=tk.LEFT)
                self.next_button.pack(side=tk.RIGHT)

    def show_image(self, image_path):
        # Load and display the image
        image = Image.open(image_path)
        image = image.resize((1550, 750))  # Adjust the size as needed
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo
        self.update_navigation_buttons()

    def show_previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image(self.image_paths[self.current_image_index])

    def show_next_image(self):
        if self.current_image_index < len(self.image_paths) - 1:
            self.current_image_index += 1
            self.show_image(self.image_paths[self.current_image_index])

    def update_navigation_buttons(self):
        if self.prev_button and self.next_button:
            if self.current_image_index == 0:
                self.prev_button.config(state=tk.DISABLED)
            else:
                self.prev_button.config(state=tk.NORMAL)

            if self.current_image_index == len(self.image_paths) - 1:
                self.next_button.config(state=tk.DISABLED)
            else:
                self.next_button.config(state=tk.NORMAL)

    def convert(self):
        # Function to handle the "Convert" menu action
        # Implement your logic here
        print("Convert menu action")

    def toggle(self):
        # Function to handle the "Toggle" menu action
        # Implement your logic here
        if self.theme == "light":
            self.theme = "dark"
        else:
            self.theme = "light"

        self.set_theme()

    def set_theme(self):
        if self.theme == "dark":
            self.root.config(bg="black")
            self.image_label.config(bg="black", fg="white")
        else:
            self.root.config(bg="white")
            self.image_label.config(bg="white", fg="black")

    def web(self):
        # Function to handle the "Web" menu action
        # Implement your logic here
        browse_into_web("https://www.google.com")

    def trends(self):
        # Function to handle the "Trends" menu action
        # Implement your logic here
        print("Trends menu action")

    def todo(self):
        # Function to handle the "To-do" menu action
        # Implement your logic here
        print("To-do menu action")

    def insert_into_db(self):
        print("Database Insert")

    def open_from_db(self):
        print("Open from Database")

    def toggle_fullscreen(self):
        # Function to handle the "Fullscreen" menu action
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))


# Create the main window
root = tk.Tk()

# Create the ImageAlbum instance
album = ImageAlbum(root)

# Start the Tkinter event loop
root.mainloop()
