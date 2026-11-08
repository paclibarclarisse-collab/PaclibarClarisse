
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


if __name__ == '__main__':
    app.run(debug=True)
