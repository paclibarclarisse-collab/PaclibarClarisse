
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


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
