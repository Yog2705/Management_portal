import os
import sqlite3
from flask import (
Flask, render_template, request, redirect, url_for, flash,jsonify,g  
)

app=Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "mevi-workshop-development-key")

#Database configuration
os.makedirs(app.instance_path, exist_ok=True)

DATABASE = os.environ.get("DATABASE_PATH",
os.path.join(app.instance_path, "management.db"))

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()  

        def init_db():
            with sqlite3.connect(DATABASE) as db:
                db.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    course TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)

@app.route("/")
def dashboard():
    db = get_db()

    total_students = db.execute("SELECT COUNT(*) FROM students").fetchone()[0]

    total_courses = db.execute("SELECT COUNT(DISTINCT course) FROM students").fetchone()[0]

    recent_students = db.execute("SELECT * FROM students ORDER BY created_at DESC LIMIT 5").fetchall()

    return render_template("index.html", total_students=total_students, total_courses=total_courses, recent_students=recent_students)

@app.route("/students")
def students():
    db = get_db()
    all_students = db.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    return render_template("students.html", students=all_students)