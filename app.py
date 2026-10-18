
import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# SQLite database connection
def get_db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Existing student API
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00270",
        "name": "Paclibar Clarisse",
        "program": "BSIT",
        "year": 3,
        "section": "DIJKSTRA"
    })


# Existing greeting API
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })


# Existing subjects API
@app.route('/subjects')
def get_subjects():
    return jsonify({
        "student": "Paclibar Clarisse",
        "subjects": [
            "Python Programming",
            "Web Development",
            "Database Management"
        ],
        "semester": "First Semester"
    })


# Existing study-hours API
@app.route('/study-hours')
def study_hours():
    subject = request.args.get('subject', 'Python')
    hours = request.args.get('hours', '2')

    return jsonify({
        "subject": subject,
        "study_hours": hours,
        "message": f"You studied {subject} for {hours} hours."
    })


# Activity 7: Get all students from SQLite database
@app.route('/students')
def get_students():
    conn = get_db_connection()
    students = conn.execute(
        'SELECT * FROM students'
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


# Activity 7: Get one student by database ID
@app.route('/students/<int:id>')
def get_student_by_id(id):
    conn = get_db_connection()
    student = conn.execute(
        'SELECT * FROM students WHERE id = ?', (id,)
    ).fetchone()
    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# Additional task: Get students by program
@app.route('/students/program/<program>')
def get_students_by_program(program):
    conn = get_db_connection()
    students = conn.execute(
        'SELECT * FROM students WHERE program = ?',
        (program.upper(),)
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


if __name__ == '__main__':
    app.run(debug=True)
