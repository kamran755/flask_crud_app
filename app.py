from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"


# ---------- DATABASE CONNECTION ----------
def get_db():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn


# ---------- CREATE TABLE IF NOT EXISTS ----------
def init_db():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        course TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()


# ---------- HOME PAGE ----------
@app.route('/')
def index():
    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template('index.html', students=students)


# ---------- ADD STUDENT ----------
@app.route('/add', methods=['POST'])
def add_student():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    course = request.form.get('course', '').strip()

    if not name or not email or not course:
        flash('All fields are required.', 'danger')
        return redirect(url_for('index'))

    conn = get_db()
    conn.execute("INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
                 (name, email, course))
    conn.commit()
    conn.close()

    flash('Student added successfully!', 'success')
    return redirect(url_for('index'))


# ---------- EDIT PAGE ----------
@app.route('/edit/<int:id>')
def edit(id):
    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()
    conn.close()

    if not student:
        flash('Student not found.', 'danger')
        return redirect(url_for('index'))

    return render_template('edit.html', student=student)


# ---------- UPDATE STUDENT ----------
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    course = request.form.get('course', '').strip()

    if not name or not email or not course:
        flash('All fields are required.', 'danger')
        return redirect(url_for('edit', id=id))

    conn = get_db()
    conn.execute("UPDATE students SET name=?, email=?, course=? WHERE id=?",
                 (name, email, course, id))
    conn.commit()
    conn.close()

    flash('Student updated successfully!', 'success')
    return redirect(url_for('index'))


# ---------- DELETE STUDENT ----------
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    flash('Student deleted!', 'success')
    return redirect(url_for('index'))


# ---------- RUN APP ----------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
