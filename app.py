import os
import sqlite3
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, jsonify, g, abort
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "change-this-secret-key-before-deployment"
)

os.makedirs(app.instance_path, exist_ok=True)
DATABASE = os.environ.get(
    "DATABASE_PATH",
    os.path.join(app.instance_path, "management.db")
)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create missing tables without deleting existing student records."""
    with sqlite3.connect(DATABASE) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                course TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                course_code TEXT NOT NULL UNIQUE,
                duration TEXT NOT NULL,
                description TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.commit()


def clean(value):
    return (value or "").strip()


# ---------------- DASHBOARD ----------------

@app.route("/")
def dashboard():
    db = get_db()

    total_students = db.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    total_courses = db.execute(
        "SELECT COUNT(*) FROM courses"
    ).fetchone()[0]

    recent_students = db.execute(
        "SELECT * FROM students ORDER BY id DESC LIMIT 5"
    ).fetchall()

    recent_courses = db.execute(
        "SELECT * FROM courses ORDER BY id DESC LIMIT 5"
    ).fetchall()

    return render_template(
        "index.html",
        total_students=total_students,
        total_courses=total_courses,
        recent_students=recent_students,
        recent_courses=recent_courses
    )


# ---------------- STUDENTS CRUD ----------------

@app.route("/students")
def students():
    db = get_db()

    all_students = db.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    return render_template(
        "students.html",
        students=all_students,
        edit_student=None
    )


@app.route("/students/add", methods=["POST"])
def add_student():
    name = clean(request.form.get("name"))
    email = clean(request.form.get("email")).lower()
    course = clean(request.form.get("course"))

    if not all([name, email, course]):
        flash("Please fill in all student fields.", "error")
        return redirect(url_for("students"))

    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("students"))

    try:
        db = get_db()

        db.execute(
            """INSERT INTO students (name, email, course)
               VALUES (?, ?, ?)""",
            (name, email, course)
        )

        db.commit()
        flash("Student added successfully.", "success")

    except sqlite3.IntegrityError:
        flash("That email address is already registered.", "error")

    return redirect(url_for("students"))


@app.route("/students/<int:student_id>/edit")
def edit_student(student_id):
    db = get_db()

    record = db.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if record is None:
        abort(404)

    all_students = db.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    return render_template(
        "students.html",
        students=all_students,
        edit_student=record
    )


@app.route("/students/<int:student_id>/update", methods=["POST"])
def update_student(student_id):
    name = clean(request.form.get("name"))
    email = clean(request.form.get("email")).lower()
    course = clean(request.form.get("course"))

    if not all([name, email, course]):
        flash("Please fill in all student fields.", "error")
        return redirect(url_for("edit_student", student_id=student_id))

    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("edit_student", student_id=student_id))

    db = get_db()

    try:
        cursor = db.execute(
            """UPDATE students
               SET name = ?, email = ?, course = ?
               WHERE id = ?""",
            (name, email, course, student_id)
        )

        db.commit()

        if cursor.rowcount == 0:
            abort(404)

        flash("Student details updated successfully.", "success")

    except sqlite3.IntegrityError:
        flash("Another student is already using that email.", "error")

    return redirect(url_for("students"))


@app.route("/students/<int:student_id>/delete", methods=["POST"])
def delete_student(student_id):
    db = get_db()

    cursor = db.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    db.commit()

    if cursor.rowcount == 0:
        abort(404)

    flash("Student deleted successfully.", "success")

    return redirect(url_for("students"))


@app.route("/api/students")
def students_api():
    rows = get_db().execute(
        """SELECT id, name, email, course, created_at
           FROM students ORDER BY id DESC"""
    ).fetchall()

    return jsonify([dict(row) for row in rows])


# ---------------- COURSES CRUD ----------------

@app.route("/courses")
def courses():
    db = get_db()

    all_courses = db.execute(
        "SELECT * FROM courses ORDER BY id DESC"
    ).fetchall()

    return render_template(
        "courses.html",
        courses=all_courses,
        edit_course=None
    )


@app.route("/courses/add", methods=["POST"])
def add_course():
    course_name = clean(request.form.get("course_name"))
    course_code = clean(request.form.get("course_code")).upper()
    duration = clean(request.form.get("duration"))
    description = clean(request.form.get("description"))

    if not all([course_name, course_code, duration]):
        flash("Course name, code and duration are required.", "error")
        return redirect(url_for("courses"))

    db = get_db()

    try:
        db.execute(
            """INSERT INTO courses
               (course_name, course_code, duration, description)
               VALUES (?, ?, ?, ?)""",
            (course_name, course_code, duration, description)
        )

        db.commit()
        flash("Course added successfully.", "success")

    except sqlite3.IntegrityError:
        flash("That course code already exists.", "error")

    return redirect(url_for("courses"))


@app.route("/courses/<int:course_id>/edit")
def edit_course(course_id):
    db = get_db()

    record = db.execute(
        "SELECT * FROM courses WHERE id = ?",
        (course_id,)
    ).fetchone()

    if record is None:
        abort(404)

    all_courses = db.execute(
        "SELECT * FROM courses ORDER BY id DESC"
    ).fetchall()

    return render_template(
        "courses.html",
        courses=all_courses,
        edit_course=record
    )


@app.route("/courses/<int:course_id>/update", methods=["POST"])
def update_course(course_id):
    course_name = clean(request.form.get("course_name"))
    course_code = clean(request.form.get("course_code")).upper()
    duration = clean(request.form.get("duration"))
    description = clean(request.form.get("description"))

    if not all([course_name, course_code, duration]):
        flash("Course name, code and duration are required.", "error")
        return redirect(url_for("edit_course", course_id=course_id))

    db = get_db()

    try:
        cursor = db.execute(
            """UPDATE courses
               SET course_name = ?, course_code = ?,
                   duration = ?, description = ?
               WHERE id = ?""",
            (course_name, course_code, duration, description, course_id)
        )

        db.commit()

        if cursor.rowcount == 0:
            abort(404)

        flash("Course updated successfully.", "success")

    except sqlite3.IntegrityError:
        flash("Another course is already using that course code.", "error")

    return redirect(url_for("courses"))


@app.route("/courses/<int:course_id>/delete", methods=["POST"])
def delete_course(course_id):
    db = get_db()

    cursor = db.execute(
        "DELETE FROM courses WHERE id = ?",
        (course_id,)
    )

    db.commit()

    if cursor.rowcount == 0:
        abort(404)

    flash("Course deleted successfully.", "success")

    return redirect(url_for("courses"))


@app.route("/api/courses")
def courses_api():
    rows = get_db().execute(
        """SELECT id, course_name, course_code, duration,
                  description, created_at
           FROM courses ORDER BY id DESC"""
    ).fetchall()

    return jsonify([dict(row) for row in rows])


# ---------------- HEALTH CHECK ----------------

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "MEVI Management Portal"
    })


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


# Initialize database without deleting existing records
init_db()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)