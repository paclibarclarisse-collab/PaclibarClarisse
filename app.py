
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to Clarisse's Flask API!"


@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00270",
        "name": "Paclibar Clarisse",
        "program": "BSIT",
        "year": 3,
        "section": "DIJKSTRA"
    })


@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })


# NEW ENDPOINT 1
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


# NEW ENDPOINT 2
@app.route('/study-hours')
def study_hours():
    subject = request.args.get('subject', 'Python')
    hours = request.args.get('hours', '2')

    return jsonify({
        "subject": subject,
        "study_hours": hours,
        "message": f"You studied {subject} for {hours} hours."
    })


if __name__ == '__main__':
    app.run(debug=True)