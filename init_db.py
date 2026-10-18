
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "students.db")

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Recreate the table to reset the IDs
cursor.execute("DROP TABLE IF EXISTS students")

cursor.execute("""
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL
)
""")

students = [
    ("2026-00123", "Juan Dela Cruz", "BSIT", 1, "A"),
    ("2026-00124", "Maria Santos", "BSIT", 1, "B"),
    ("2026-00125", "Pedro Reyes", "BSCS", 2, "A"),
    ("2026-00126", "Ana Garcia", "BSIT", 3, "C"),
    ("2026-00127", "Mark Ramos", "BSCS", 2, "B")
]

cursor.executemany("""
INSERT INTO students
(student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
""", students)

conn.commit()
conn.close()

print("Database recreated successfully!")
