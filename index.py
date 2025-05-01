import csv
from datetime import datetime
import sqlite3
from datetime import datetime
import qrcode
import cv2
import pandas as pd

ATTENDANCE_FILE = "attendance.csv"
def initialize_csv():
    try:
        with open(ATTENDANCE_FILE, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Date", "Time"])
    except FileExistsError:
        pass
def mark_attendance(name):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    with open(ATTENDANCE_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, date, time])
    print(f"Attendance marked for {name} on {date} at {time}")

def view_attendance():
    try:
        with open(ATTENDANCE_FILE, "r") as file:
            reader = csv.reader(file)
            print("\nAttendance Records:")
            for row in reader:
                print(", ".join(row))
    except FileNotFoundError:
        print("No attendance records found!")
def attendance_system():
    initialize_csv()
    while True:
        print("\nAttendance System")
        print("1. Mark Attendance")
        print("2. View Attendance")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter your name: ").strip()
            mark_attendance(name)
        elif choice == "2":
            view_attendance()
        elif choice == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    attendance_system()
    def mark_attendance_unique(name):
     today = datetime.now().strftime("%Y-%m-%d")
    try:
        with open(ATTENDANCE_FILE, "r") as file:
            reader = csv.reader(file)
            if any(row[0] == name and row[1] == today for row in reader):
                print(f"{name} has already been marked present today.")
    except FileNotFoundError:
        pass
    mark_attendance(name)

def initialize_database():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            time TEXT
        )
    """)
    conn.commit()
    conn.close()

def mark_attendance(name):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date, time))
    conn.commit()
    conn.close()
    print(f"Attendance marked for {name} on {date} at {time}")

def view_attendance():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, date, time FROM attendance")
    rows = cursor.fetchall()
    conn.close()
    print("\nAttendance Records:")
    for row in rows:
        print(", ".join(row))

def attendance_system():
    initialize_database()
    while True:
        print("\nAttendance System")
        print("1. Mark Attendance")
        print("2. View Attendance")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter your name: ").strip()
            mark_attendance(name)
        elif choice == "2":
            view_attendance()
        elif choice == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    attendance_system()


def generate_qr(data, filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
def recognize_face():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    
    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

    def generate_report(data, filename):
       df = pd.DataFrame(data)
    print(f"Report saved as {filename}")

