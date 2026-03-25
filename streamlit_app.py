import streamlit as st
import sqlite3

DB_NAME = "sms.db"

# ---------------- DB ----------------
def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

conn = get_conn()
c = conn.cursor()

# Create tables
c.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS courses (name TEXT PRIMARY KEY, capacity INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS fees (student_id INTEGER, amount INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS books (isbn TEXT PRIMARY KEY, title TEXT, status TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS scores (student_id INTEGER, score INTEGER)")
conn.commit()

# ---------------- UI ----------------
st.set_page_config(page_title="SMS Dashboard", layout="wide")
st.title("🎓 Meru University SMS")

menu = st.sidebar.selectbox("Select Module", [
    "Students", "Courses", "Fees", "Library", "Performance"
])

# ---------------- STUDENTS ----------------
if menu == "Students":
    st.header("Student Management")

    col1, col2 = st.columns(2)
    with col1:
        student_id = st.number_input("Student ID", step=1)
    with col2:
        name = st.text_input("Student Name")

    if st.button("Add Student"):
        c.execute("INSERT OR IGNORE INTO students VALUES (?,?)", (student_id, name))
        conn.commit()
        st.success("Student added!")

    st.subheader("All Students")
    students = c.execute("SELECT * FROM students").fetchall()
    st.table(students)

# ---------------- COURSES ----------------
elif menu == "Courses":
    st.header("Course Management")

    name = st.text_input("Course Name")
    capacity = st.number_input("Capacity", step=1)

    if st.button("Add Course"):
        c.execute("INSERT OR IGNORE INTO courses VALUES (?,?)", (name, capacity))
        conn.commit()
        st.success("Course added!")

    st.subheader("All Courses")
    courses = c.execute("SELECT * FROM courses").fetchall()
    st.table(courses)

# ---------------- FEES ----------------
elif menu == "Fees":
    st.header("Fee Management")

    student = st.number_input("Student ID", step=1)
    amount = st.number_input("Amount", step=1)

    if st.button("Add Fee"):
        c.execute("INSERT INTO fees VALUES (?,?)", (student, amount))
        conn.commit()
        st.success("Payment added!")

    st.subheader("All Payments")
    fees = c.execute("SELECT * FROM fees").fetchall()
    st.table(fees)

# ---------------- LIBRARY ----------------
elif menu == "Library":
    st.header("Library Management")

    isbn = st.text_input("ISBN")
    title = st.text_input("Book Title")

    if st.button("Add Book"):
        c.execute("INSERT OR IGNORE INTO books VALUES (?,?,?)", (isbn, title, "available"))
        conn.commit()
        st.success("Book added!")

    if st.button("Return All Books"):
        c.execute("UPDATE books SET status='available'")
        conn.commit()
        st.success("Books returned!")

    st.subheader("Library")
    books = c.execute("SELECT * FROM books").fetchall()
    st.table(books)

# ---------------- PERFORMANCE ----------------
elif menu == "Performance":
    st.header("Performance Analytics")

    student = st.number_input("Student ID", step=1)
    score = st.number_input("Score", step=1)

    if st.button("Add Score"):
        c.execute("INSERT INTO scores VALUES (?,?)", (student, score))
        conn.commit()
        st.success("Score added!")

    st.subheader("Top Student")
    top = c.execute("SELECT student_id, MAX(score) FROM scores").fetchone()
    st.write(top)