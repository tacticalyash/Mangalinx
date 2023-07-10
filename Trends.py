import tkinter as tk
from tkinter import ttk
import sqlite3
import patoolib
import tempfile

# Create a temporary directory to store the extracted files
temp_dir = tempfile.TemporaryDirectory()

# Connect to the SQLite database
connection = sqlite3.connect('users_data.db')
cursor = connection.cursor()

# Retrieve the column names from the database
table_name = 'namb'
cursor.execute(f"PRAGMA table_info({table_name})")
columns = [column[1] for column in cursor.fetchall()]

# Create the Tkinter window
window = tk.Tk()
window.title('Database Viewer')

# Create the ComboBox to select a column
column_combo = ttk.Combobox(window, values=columns)
column_combo.pack()

# Function to select the CBZ file and display its contents
def select_and_show():
    selected_column = column_combo.get()
    cursor.execute(f"SELECT {selected_column} FROM {table_name}")
    blob_data = cursor.fetchone()[0]

    # Save the CBZ file to a temporary file
    cbz_file = tempfile.NamedTemporaryFile(delete=False, suffix='.cbz')
    cbz_file.write(blob_data)
    cbz_file.close()

    # Extract the contents of the CBZ file using patoolib
    extracted_files = patoolib.extract_archive(cbz_file.name, outdir=temp_dir.name)

    # Display the extracted files one by one
    content_text.delete('1.0', tk.END)
    for extracted_file in extracted_files:
        content_text.insert(tk.END, f"- {extracted_file}\n")
        window.update()
        content_text.after(1000)  # Delay between displaying each file

# Create the "Select" button
select_button = tk.Button(window, text='Select', command=select_and_show)
select_button.pack()

# Create a text widget to display the extracted files
content_text = tk.Text(window)
content_text.pack()

window.mainloop()

# Close the database connection and delete the temporary directory
connection.close()
temp_dir.cleanup()
