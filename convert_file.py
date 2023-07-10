import tkinter as tk
from tkinter import filedialog
import sqlite3
import tempfile
import patoolib

# Function to handle the browse button
def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(tk.END, file_path)

# Function to handle the save button
def save_file():
    file_path = entry_path.get()
    if file_path:
        # Prompt the user to enter table name and column name
        table_name = table_var.get()
        column_name = column_entry.get()

        try:
            # Read the file content
            with open(file_path, 'rb') as file:
                file_content = file.read()

            # Save the file content in the database
            connection = sqlite3.connect('users_data.db')
            cursor = connection.cursor()

            # Create the table with a BLOB column
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_name} BLOB)"
            cursor.execute(create_table_query)

            # Insert the file content into the table
            cursor.execute(f"INSERT INTO {table_name} ({column_name}) VALUES (?)", (file_content,))

            connection.commit()
            connection.close()
            print("File saved successfully!")
        except (sqlite3.Error, IOError) as error:
            print("Error while connecting to the database or reading the file:", error)

# Function to handle the open button
def open_file():
    # Prompt the user to select table and column
    table_name = table_var.get()
    column_name = column_entry.get()

    try:
        # Retrieve the file content from the database
        connection = sqlite3.connect('users_data.db')
        cursor = connection.cursor()

        cursor.execute(f"SELECT {column_name} FROM {table_name}")
        file_content = cursor.fetchone()[0]

        connection.close()

        # Save the file content to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(file_content)
        temp_file.close()

        # Extract the CBR file using patoolib
        extracted_path = tempfile.mkdtemp()
        patoolib.extract_archive(temp_file.name, outdir=extracted_path)

        print("File opened successfully!")
    except (sqlite3.Error, IOError) as error:
        print("Error while connecting to the database or extracting the file:", error)

# Create the main window
window = tk.Tk()
window.title("File Database")
window.geometry("400x300")

# Create the browse button
btn_browse = tk.Button(window, text="Browse", command=browse_file)
btn_browse.pack(pady=10)

# Create the entry field
entry_path = tk.Entry(window, width=40)
entry_path.pack()

# Create a label for table name
label_table = tk.Label(window, text="Enter Table Name:")
label_table.pack()

# Create the table name entry field
table_var = tk.StringVar()
entry_table = tk.Entry(window, textvariable=table_var, width=30)
entry_table.pack()

# Create a label for column name
label_column = tk.Label(window, text="Enter Column Name:")
label_column.pack()

# Create the column name entry field
column_entry = tk.Entry(window, width=30)
column_entry.pack()

# Create the save button
btn_save = tk.Button(window, text="Save", command=save_file)
btn_save.pack(pady=10)

# Create the open button
btn_open = tk.Button(window, text="Open", command=open_file)
btn_open.pack(pady=10)

# Start the main loop
window.mainloop()
