from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(90), unique = True, nullable = False)
    age = db.Column(db.Integer, unique = False, nullable = False)
    city = db.Column(db.String(90), unique = False, nullable = False)

with app.app_context():
    db.create_all()

@app.route('/', methods = ['GET'])
def home():
    tasks = Task.query.all()
    tasks_lst = [{"id": task.id, "name": task.name, "age": task.age, "city": task.city} for task in tasks]
    return jsonify(tasks_lst), 200

@app.route('/students', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('age') or not data.get('city'):
        return jsonify({"error": "Name and description are required"}), 400
    task = Task(name = data['name'], age = data['age'], city = data['city'])
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created successfully", "task": {"id": task.id, "name": task.name, "age": task.age, "city": task.city}}), 201

@app.route('/students/<int:students_id>', methods = ['GET'])
def get_task(students_id):
    students = Task.query.get(students_id)
    if not students:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"id": students.id, "name": students.name, "age": students.age, "city": students.city}), 200
    

# if __name__ == '__main__':
    app.run(debug=True)