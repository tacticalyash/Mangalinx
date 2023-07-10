import tkinter as tk
import random

# Create the Tkinter window
window = tk.Tk()
window.title("Welcome to the Manga world!")

# Define the size of each box
box_size = 19

# Create a scrollable canvas
canvas = tk.Canvas(window)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a scrollbar
scrollbar = tk.Scrollbar(window, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas to use the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a frame to hold the boxes
frame = tk.Frame(canvas)
frame.pack()

# Calculate the number of rows and columns
num_rows = 5
num_cols = 6

# Create 30 boxes in a 6x5 format
for i in range(30):
    # Calculate the row and column indices
    row = i // num_cols
    col = i % num_cols

    # Generate a random number
    random_number = random.randint(1, 100)

    # Create a box label with the random number
    box = tk.Label(frame, text=random_number, width=box_size, height=box_size, borderwidth=1, relief="solid")
    box.grid(row=row, column=col, padx=5, pady=5)  # Add padding between the boxes

# Configure the scrollbar to scroll the canvas
canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scrollbar.set)

# Start the Tkinter event loop
window.mainloop()
