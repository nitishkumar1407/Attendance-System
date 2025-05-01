import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost", 
    user="root",       
    password="950811****",  
    database="new_attendance_system"   
)
cursor = db_connection.cursor()

# Fetch students from the database
def fetch_students():
    cursor.execute("SELECT name, roll_number FROM new_students ORDER BY name;")
    return cursor.fetchall()

# Mark attendance in the database
def mark_attendance():
    selected_roll = roll_var.get()
    status = status_var.get()
    date = datetime.now().strftime('%Y-%m-%d')
    
    if not selected_roll or not status:
        messagebox.showwarning("Input Error", "Please select both Roll Number and Status")
        return
    
    try:
        cursor.execute(
            "INSERT INTO new_attendance (roll_number, attendance_status, date) VALUES (%s, %s, %s)",
            (selected_roll, status, date)
        )
        db_connection.commit()
        messagebox.showinfo("Success", f"Attendance marked: Roll Number {selected_roll} as {status} on {date}.")
        update_attendance_table()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Fetch attendance records
def fetch_attendance():
    cursor.execute(
        """
        SELECT a.attendance_id, s.name, a.roll_number, a.attendance_status, a.date 
        FROM new_attendance a 
        JOIN new_students s ON a.roll_number = s.roll_number 
        ORDER BY a.date DESC, s.name;
        """
    )
    return cursor.fetchall()

# Update attendance table in UI
def update_attendance_table():
    for row in attendance_tree.get_children():
        attendance_tree.delete(row)
    for record in fetch_attendance():
        attendance_tree.insert("", "end", values=record)

# GUI Setup
root = tk.Tk()
root.title("Attendance Management System")
root.geometry("600x500")

# Dropdown for selecting student
students = fetch_students()
roll_var = tk.StringVar()
status_var = tk.StringVar()

tk.Label(root, text="Select Roll Number:").pack()
roll_dropdown = ttk.Combobox(root, textvariable=roll_var, values=[s[1] for s in students])
roll_dropdown.pack()

tk.Label(root, text="Select Status:").pack()
status_dropdown = ttk.Combobox(root, textvariable=status_var, values=["Present", "Absent"])
status_dropdown.pack()

tk.Button(root, text="Mark Attendance", command=mark_attendance).pack(pady=10)

# Attendance Record Table
attendance_tree = ttk.Treeview(root, columns=("ID", "Name", "Roll Number", "Status", "Date"), show="headings")
for col in ("ID", "Name", "Roll Number", "Status", "Date"):
    attendance_tree.heading(col, text=col)
    attendance_tree.column(col, width=100)
attendance_tree.pack(expand=True, fill=tk.BOTH)

update_attendance_table()

root.mainloop()

# Close database connection
cursor.close()
db_connection.close()


