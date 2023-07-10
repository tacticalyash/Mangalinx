import sqlite3
import patoolib
import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import io
import tempfile

# Connect to the SQLite database
conn = sqlite3.connect('users_data.db')
cursor = conn.cursor()

# Retrieve the BLOB files from the database
cursor.execute("SELECT FF FROM namb")
result = cursor.fetchall()

# Create the main window
window = tk.Tk()
window.title("Extracted Images")

# Create a scrollable canvas
canvas = tk.Canvas(window)
scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Store the BLOB data in a list
blob_data_list = []

# Iterate over the results and store the BLOB data in the list
for row in result:
    blob_data = row[0]  # Assuming the BLOB data is stored in the first column
    blob_data_list.append(blob_data)

def extract_selected_file():
    selected_index = int(selected_blob_var.get()) - 1
    blob_data = blob_data_list[selected_index]
    
    # Create a temporary file to save the BLOB data
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(blob_data)
    temp_file.close()
    
    # Get the original file path and format
    original_file_path = get_original_file_path(temp_file.name)  # Replace with your logic to get the original file path
    original_file_format = os.path.splitext(original_file_path)[1].lower()

    if original_file_format in ['.cbz', '.cbr']:
        # Extract images using patoolib
        extracted_directory = 'extracted_images'
        patoolib.extract_archive(original_file_path, outdir=extracted_directory)
        
        # Display the extracted images in the scrollable frame
        display_images_from_directory(extracted_directory, scrollable_frame)

    # Remove the temporary file
    os.remove(temp_file.name)

# Create a ComboBox to select the BLOB file
selected_blob_var = tk.StringVar()
selected_blob_combobox = ttk.Combobox(window, textvariable=selected_blob_var)
selected_blob_combobox['values'] = list(range(1, len(blob_data_list) + 1))  # Add the indices of the BLOB files here
selected_blob_combobox.pack()

# Create an OK button to extract the selected file
ok_button = tk.Button(window, text="OK", command=extract_selected_file)
ok_button.pack()

def get_original_file_path(temp_file_path):
    # Replace this logic with your own to retrieve the original file path associated with the BLOB data
    # You can use the provided temp_file_path as a reference to retrieve the original file path
    pass

def display_images_from_directory(directory, parent_frame):
    for filename in os.listdir(directory):
        image_path = os.path.join(directory, filename)
        image = Image.open(image_path)
        image = image.resize((200, 200))  # Resize the image as needed
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(parent_frame, image=photo)
        label.image = photo  # Store a reference to prevent garbage collection
        label.pack()

# Start the Tkinter event loop
window.mainloop()
