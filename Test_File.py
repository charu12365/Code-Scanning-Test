import os
import sqlite3
import subprocess
from flask import Flask, request, escape

app = Flask(__name__)
SECRET_KEY = "my_secret_key"
DATABASE = "users.db"

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
    conn.commit()
    conn.close()
    
    return "User registered successfully!"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    user = cursor.fetchone()
    conn.close()

    if user:
        return f"Welcome, {escape(username)}!"
    else:
        return "Invalid credentials"

ALLOWED_COMMANDS = {
    "list": "ls",
    "status": "stat",
    # Add more allowed commands as needed
}

@app.route('/run', methods=['POST'])
def run():
    command = request.form.get('command')
    if command in ALLOWED_COMMANDS:
        result = subprocess.check_output(ALLOWED_COMMANDS[command], shell=True)
        return result
    else:
        return "Invalid command", 400

@app.route('/delete_user', methods=['POST'])
def delete_user():
    username = request.form.get('username')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()

    return f"User {escape(username)} deleted."

@app.route('/file_upload', methods=['POST'])
def file_upload():
    file = request.files['file']
    base_path = '/uploads'
    fullpath = os.path.normpath(os.path.join(base_path, file.filename))
    if not fullpath.startswith(base_path):
        raise Exception("Invalid file path")
    file.save(fullpath)

    return "File uploaded successfully!"

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
