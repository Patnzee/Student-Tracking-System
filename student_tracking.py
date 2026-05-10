import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# Connect to the SQLite database
connection = sqlite3.connect("student_tracking.db")
cursor = connection.cursor()

# Create the students table if it does not already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email TEXT NOT NULL,
    current_course TEXT NOT NULL
)
""")

connection.commit()


# Function to add a new student
def add_student():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    phone_number = phone_entry.get()
    email = email_entry.get()
    current_course = course_entry.get()

    # Check that all boxes have been filled in
    if first_name == "" or last_name == "" or phone_number == "" or email == "" or current_course == "":
        messagebox.showwarning("Missing Information", "Please complete all fields.")
        return

    # Insert the student details into the database
    cursor.execute("""
    INSERT INTO students (first_name, last_name, phone_number, email, current_course)
    VALUES (?, ?, ?, ?, ?)
    """, (first_name, last_name, phone_number, email, current_course))

    connection.commit()

    clear_form()
    show_students()


# Function to clear the form after submitting
def clear_form():
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)


# Function to show all students in the table
def show_students():
    # Clear the current table first
    for item in student_table.get_children():
        student_table.delete(item)

    # Get all students from the database
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    # Add each student to the table
    for student in students:
        student_table.insert("", tk.END, values=student)


# Function to delete a selected student
def delete_student():
    selected_student = student_table.selection()

    if not selected_student:
        messagebox.showwarning("No Student Selected", "Please select a student to delete.")
        return

    student_id = student_table.item(selected_student)["values"][0]

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    connection.commit()

    show_students()
    messagebox.showinfo("Deleted", "Student record has been deleted.")


# Main window
root = tk.Tk()
root.title("Student Tracking")
root.geometry("900x550")
root.configure(bg="#dceeff")

# Title
title_label = tk.Label(
    root,
    text="Student Tracking",
    font=("Arial", 24, "bold"),
    bg="#dceeff",
    fg="#1b3a57"
)
title_label.pack(pady=15)

# Form area
form_frame = tk.Frame(root, bg="#dceeff")
form_frame.pack(pady=10)

label_style = {
    "bg": "#dceeff",
    "fg": "#1b3a57",
    "font": ("Arial", 11)
}

tk.Label(form_frame, text="First Name", **label_style).grid(row=0, column=0, padx=10, pady=5, sticky="e")
first_name_entry = tk.Entry(form_frame, width=30)
first_name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Last Name", **label_style).grid(row=1, column=0, padx=10, pady=5, sticky="e")
last_name_entry = tk.Entry(form_frame, width=30)
last_name_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Phone Number", **label_style).grid(row=2, column=0, padx=10, pady=5, sticky="e")
phone_entry = tk.Entry(form_frame, width=30)
phone_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Email", **label_style).grid(row=3, column=0, padx=10, pady=5, sticky="e")
email_entry = tk.Entry(form_frame, width=30)
email_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Current Course", **label_style).grid(row=4, column=0, padx=10, pady=5, sticky="e")
course_entry = tk.Entry(form_frame, width=30)
course_entry.grid(row=4, column=1, padx=10, pady=5)

# Button area
button_frame = tk.Frame(root, bg="#dceeff")
button_frame.pack(pady=10)

submit_button = tk.Button(
    button_frame,
    text="Submit",
    width=15,
    bg="#2f80ed",
    fg="white",
    command=add_student
)
submit_button.grid(row=0, column=0, padx=10)

delete_button = tk.Button(
    button_frame,
    text="Delete Selected",
    width=15,
    bg="#d9534f",
    fg="white",
    command=delete_student
)
delete_button.grid(row=0, column=1, padx=10)

# Table area
table_frame = tk.Frame(root)
table_frame.pack(pady=15, padx=20, fill="both", expand=True)

student_table = ttk.Treeview(
    table_frame,
    columns=("ID", "First Name", "Last Name", "Phone Number", "Email", "Current Course"),
    show="headings"
)

student_table.heading("ID", text="ID")
student_table.heading("First Name", text="First Name")
student_table.heading("Last Name", text="Last Name")
student_table.heading("Phone Number", text="Phone Number")
student_table.heading("Email", text="Email")
student_table.heading("Current Course", text="Current Course")

student_table.column("ID", width=50)
student_table.column("First Name", width=120)
student_table.column("Last Name", width=120)
student_table.column("Phone Number", width=130)
student_table.column("Email", width=200)
student_table.column("Current Course", width=160)

student_table.pack(fill="both", expand=True)

# Display saved students when the app opens
show_students()

# Start the program
root.mainloop()

# Close the database connection when the app is closed
connection.close()