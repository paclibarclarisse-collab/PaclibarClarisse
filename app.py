
import sqlite3
import json
from urllib.request import urlopen

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


# Activity 7: Get all students
@app.route('/students')
def get_students():
    conn = get_db_connection()
    students = conn.execute(
        'SELECT * FROM students'
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


# Activity 7: Get one student
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


# Activity 7: Search students by program
@app.route('/students/program/<program>')
def get_students_by_program(program):
    conn = get_db_connection()
    students = conn.execute(
        'SELECT * FROM students WHERE program = ?',
        (program.upper(),)
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


# Activity 8: READ ALL STUDENTS
@app.route('/api/students', methods=['GET'])
def api_get_all_students():
    conn = get_db_connection()
    students = conn.execute(
        'SELECT * FROM students'
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


# Activity 8: CREATE
@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.execute(
        """INSERT INTO students
        (student_id, name, program, year, section)
        VALUES (?, ?, ?, ?, ?)""",
        (
            data['student_id'],
            data['name'],
            data['program'],
            data['year'],
            data['section']
        )
    )

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Student added",
        "id": new_id
    }), 201


# Activity 8: READ ONE STUDENT
@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    conn = get_db_connection()
    student = conn.execute(
        'SELECT * FROM students WHERE id = ?', (id,)
    ).fetchone()
    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# Activity 8: UPDATE
@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()

    conn = get_db_connection()
    conn.execute(
        """UPDATE students SET student_id=?, name=?, program=?,
        year=?, section=? WHERE id=?""",
        (
            data['student_id'],
            data['name'],
            data['program'],
            data['year'],
            data['section'],
            id
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Student updated"})


# Activity 8: DELETE
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()
    conn.execute(
        'DELETE FROM students WHERE id = ?', (id,)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Student deleted"})


# Activity 8: RETRIEVE CLASSMATE'S RECORDS
@app.route('/api/classmate-students', methods=['GET'])
def get_classmate_students():
    classmate_url = "https://flask-malunes-act4.onrender.com/student"

    try:
        with urlopen(classmate_url, timeout=30) as response:
            students = json.loads(
                response.read().decode('utf-8')
            )

        return jsonify(students)

    except Exception as error:
        return jsonify({
            "error": "Unable to retrieve classmate records",
            "details": str(error)
        }), 500


# Activity 8: SAVE CLASSMATE'S RECORD TO MY DATABASE
@app.route('/api/classmate-students/save', methods=['POST'])
def save_classmate_student():
    classmate_url = "https://flask-malunes-act4.onrender.com/student"

    try:
        # Retrieve classmate's information
        with urlopen(classmate_url, timeout=30) as response:
            student = json.loads(
                response.read().decode('utf-8')
            )

        # Check if the student already exists
        conn = get_db_connection()

        existing = conn.execute(
            'SELECT id FROM students WHERE student_id = ?',
            (student['student_id'],)
        ).fetchone()

        if existing:
            conn.close()
            return jsonify({
                "message": "This student is already saved in your database."
            }), 409

        # Save classmate's information
        conn.execute(
            """INSERT INTO students
            (student_id, name, program, year, section)
            VALUES (?, ?, ?, ?, ?)""",
            (
                student['student_id'],
                student['name'],
                student['program'],
                student['year'],
                student['section']
            )
        )

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Classmate's record successfully saved!",
            "student": student
        }), 201

    except Exception as error:
        return jsonify({
            "error": "Unable to save classmate's record",
            "details": str(error)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
