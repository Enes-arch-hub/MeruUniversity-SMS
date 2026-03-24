from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_NAME = "sms.db"

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Students
    c.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT)")
    # Courses
    c.execute("CREATE TABLE IF NOT EXISTS courses (name TEXT PRIMARY KEY, capacity INTEGER)")
    # Registrations
    c.execute("CREATE TABLE IF NOT EXISTS registrations (student_id INTEGER, course TEXT)")
    # Fees
    c.execute("CREATE TABLE IF NOT EXISTS fees (student_id INTEGER, amount INTEGER)")
    # Library
    c.execute("CREATE TABLE IF NOT EXISTS books (isbn TEXT PRIMARY KEY, title TEXT, status TEXT)")
    # Performance
    c.execute("CREATE TABLE IF NOT EXISTS scores (student_id INTEGER, score INTEGER)")
    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

# Students
@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.get_json()
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO students (id,name) VALUES (?,?)", (data["id"], data["name"]))
        conn.commit()
    return jsonify({"message":"Student added"})

@app.route("/all_students")
def all_students():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id,name FROM students")
    students = [{"id": row[0], "name": row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify({"students": students})

# Courses
@app.route("/add_course", methods=["POST"])
def add_course():
    data = request.get_json()
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO courses (name,capacity) VALUES (?,?)", (data["name"], data["capacity"]))
        conn.commit()
    return jsonify({"message":"Course added"})

@app.route("/get_courses")
def get_courses():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name,capacity FROM courses")
    courses = [{"name":row[0], "capacity":row[1], "enrolled":0} for row in c.fetchall()]
    conn.close()
    return jsonify({"courses": courses})

# Fees
@app.route("/add_fee", methods=["POST"])
def add_fee():
    data = request.get_json()
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO fees (student_id,amount) VALUES (?,?)", (data["student"], data["amount"]))
        conn.commit()
    return jsonify({"message":"Fee added"})

@app.route("/get_fees")
def get_fees():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT student_id, amount FROM fees")
    fees = [{"student":row[0], "amount":row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify({"fees": fees})

# Library
@app.route("/add_book", methods=["POST"])
def add_book():
    data = request.get_json()
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO books (isbn,title,status) VALUES (?,?,?)", (data["isbn"], data["title"], "available"))
        conn.commit()
    return jsonify({"message":"Book added"})

@app.route("/get_books")
def get_books():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT isbn,title,status FROM books")
    books = [{"isbn":row[0], "title":row[1], "status":row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify({"books": books})

@app.route("/borrow_book", methods=["POST"])
def borrow_book():
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE books SET status='borrowed' WHERE isbn=? AND status='available'", (data["isbn"],))
    conn.commit()
    conn.close()
    return jsonify({"message":"Book borrowed"})

@app.route("/return_book", methods=["POST"])
def return_book():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE books SET status='available' WHERE status='borrowed'")
    conn.commit()
    conn.close()
    return jsonify({"message":"Books returned"})
    
# Performance
@app.route("/add_score", methods=["POST"])
def add_score():
    data = request.get_json()
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO scores (student_id,score) VALUES (?,?)", (data["student"], data["score"]))
        conn.commit()
    return jsonify({"message":"Score added"})

@app.route("/top_student")
def top_student():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT student_id, MAX(score) FROM scores")
    row = c.fetchone()
    conn.close()
    if row[0]:
        return jsonify({"top":{"id":row[0], "name":"Unknown","score":row[1]}})
    return jsonify({"top":{}})

# Run server
if __name__ == "__main__":
    app.run(debug=True)