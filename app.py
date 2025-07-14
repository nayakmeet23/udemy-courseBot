from flask import Flask, jsonify
from udemypy.database import database

app = Flask(__name__)

@app.route('/')
def home():
    return "UdemyPy Web Server is running!"

@app.route('/courses')
def list_courses():
    db = database.connect()
    courses = database.retrieve_courses(db)
    # Convert Course objects to dicts for JSON serialization
    return jsonify({'courses': [vars(c) for c in courses]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 