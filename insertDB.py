import tkinter as tk
from tkinter import ttk
import sqlite3

def show_table():
    selected_table = combo_box.get()
    if selected_table:
        # Connect to the SQLite database
        conn = sqlite3.connect("users_data.db")
        cursor = conn.cursor()

        # Fetch the column names from the selected table
        cursor.execute(f"SELECT * FROM {selected_table}")
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

        # Close the database connection
        conn.close()

        # Display the column names and rows in a table format
        print("Columns:", column_names)
        print("Rows:")
        for row in rows:
            print(row)
    else:
        print("No table selected")

# Connect to the SQLite database
conn = sqlite3.connect("users_data.db")
cursor = conn.cursor()

# Fetch the table names from the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
table_names = [table[0] for table in tables]

# Create the main window
root = tk.Tk()

# Create a ComboBox to select the table
combo_box = ttk.Combobox(root, values=table_names, width=30)
combo_box.pack()

# Create a button to show the table
show_button = ttk.Button(root, text="Show Table", command=show_table)
show_button.pack()

# Create a Label to display the column names
columns_label = ttk.Label(root, text="Columns:")
columns_label.pack()

# Create a circular ComboBox to display the column names
columns_combo_box = ttk.Combobox(root, values=[], width=30, state="readonly")
columns_combo_box.pack()

# Update the column names in the circular ComboBox based on the selected table
def update_columns(event):
    selected_table = combo_box.get()
    if selected_table:
        # Connect to the SQLite database
        conn = sqlite3.connect("users_data.db")
        cursor = conn.cursor()

        # Fetch the column names from the selected table
        cursor.execute(f"PRAGMA table_info({selected_table})")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]

        # Close the database connection
        conn.close()

        # Update the column names in the circular ComboBox
        columns_combo_box['values'] = column_names
        columns_combo_box.current(0)  # Select the first column by default
    else:
        columns_combo_box['values'] = []

combo_box.bind("<<ComboboxSelected>>", update_columns)

# Close the database connection
conn.close()

# Start the Tkinter event loop
root.mainloop()
