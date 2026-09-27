from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db, init_db
from datetime import date as today_date

app = Flask(__name__)
app.secret_key = "secret_key_attendance"


# ============================================================
# DASHBOARD
# ============================================================
@app.route("/")
def index():
    conn = get_db()

    total_students = conn.execute("SELECT COUNT(*) AS c FROM students").fetchone()["c"]
    total_subjects = conn.execute("SELECT COUNT(*) AS c FROM subjects").fetchone()["c"]
    total_records  = conn.execute("SELECT COUNT(*) AS c FROM attendance").fetchone()["c"]

    today = today_date.today().isoformat()
    today_present = conn.execute(
        "SELECT COUNT(*) AS c FROM attendance WHERE date=? AND status='Present'",
        (today,)
    ).fetchone()["c"]
    today_absent = conn.execute(
        "SELECT COUNT(*) AS c FROM attendance WHERE date=? AND status='Absent'",
        (today,)
    ).fetchone()["c"]

    top_students = conn.execute("""
        SELECT s.name, s.roll_no,
               ROUND(100.0 * SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END) / COUNT(a.id), 1) AS pct
        FROM students s
        JOIN attendance a ON s.id = a.student_id
        GROUP BY s.id
        ORDER BY pct DESC
        LIMIT 5
    """).fetchall()

    recent = conn.execute("""
        SELECT a.date, s.name AS student, sub.code AS subject, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        JOIN subjects sub ON a.subject_id = sub.id
        ORDER BY a.id DESC
        LIMIT 5
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        total_students=total_students,
        total_subjects=total_subjects,
        total_records=total_records,
        today_present=today_present,
        today_absent=today_absent,
        today=today,
        top_students=top_students,
        recent=recent
    )


# ============================================================
# STUDENTS
# ============================================================
@app.route("/students", methods=["GET", "POST"])
def students():
    conn = get_db()
    if request.method == "POST":
        roll  = request.form["roll_no"].strip()
        name  = request.form["name"].strip()
        cls   = request.form.get("class_name", "").strip()
        email = request.form.get("email", "").strip()
        try:
            conn.execute(
                "INSERT INTO students (roll_no, name, class_name, email) VALUES (?,?,?,?)",
                (roll, name, cls, email)
            )
            conn.commit()
            flash(f"✅ Student '{name}' added successfully!", "success")
        except Exception as e:
            flash(f"⚠️ Error: {e}", "danger")
    rows = conn.execute("SELECT * FROM students ORDER BY roll_no").fetchall()
    conn.close()
    return render_template("students.html", students=rows)


@app.route("/students/delete/<int:sid>")
def delete_student(sid):
    conn = get_db()
    conn.execute("DELETE FROM attendance WHERE student_id=?", (sid,))
    conn.execute("DELETE FROM students WHERE id=?", (sid,))
    conn.commit()
    conn.close()
    flash("🗑️ Student deleted successfully.", "info")
    return redirect(url_for("students"))


# ============================================================
# SUBJECTS
# ============================================================
@app.route("/subjects", methods=["GET", "POST"])
def subjects():
    conn = get_db()
    if request.method == "POST":
        code    = request.form["code"].strip()
        name    = request.form["name"].strip()
        faculty = request.form.get("faculty", "").strip()
        try:
            conn.execute(
                "INSERT INTO subjects (code, name, faculty) VALUES (?,?,?)",
                (code, name, faculty)
            )
            conn.commit()
            flash(f"✅ Subject '{name}' added!", "success")
        except Exception as e:
            flash(f"⚠️ Error: {e}", "danger")
    rows = conn.execute("SELECT * FROM subjects ORDER BY code").fetchall()
    conn.close()
    return render_template("subjects.html", subjects=rows)


@app.route("/subjects/delete/<int:sid>")
def delete_subject(sid):
    conn = get_db()
    conn.execute("DELETE FROM attendance WHERE subject_id=?", (sid,))
    conn.execute("DELETE FROM subjects WHERE id=?", (sid,))
    conn.commit()
    conn.close()
    flash("🗑️ Subject deleted.", "info")
    return redirect(url_for("subjects"))


# ============================================================
# ATTENDANCE
# ============================================================
@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    conn = get_db()
    students_list = conn.execute("SELECT * FROM students ORDER BY roll_no").fetchall()
    subjects_list = conn.execute("SELECT * FROM subjects ORDER BY code").fetchall()

    if request.method == "POST":
        date = request.form["date"]
        subject_id = request.form["subject_id"]
        saved = 0
        for s in students_list:
            status = request.form.get(f"status_{s['id']}")
            if status:
                conn.execute("""
                    INSERT INTO attendance (student_id, subject_id, date, status)
                    VALUES (?,?,?,?)
                    ON CONFLICT(student_id, subject_id, date)
                    DO UPDATE SET status=excluded.status
                """, (s["id"], subject_id, date, status))
                saved += 1
        conn.commit()
        flash(f"✅ Attendance saved for {saved} student(s) on {date}.", "success")

    conn.close()
    return render_template(
        "attendance.html",
        students=students_list,
        subjects=subjects_list,
        today=today_date.today().isoformat()
    )


# ============================================================
# DATE-WISE
# ============================================================
@app.route("/datewise")
def datewise():
    conn = get_db()
    date = request.args.get("date", "")
    subject_id = request.args.get("subject_id", "")
    subjects_list = conn.execute("SELECT * FROM subjects ORDER BY code").fetchall()

    records = []
    if date:
        query = """
            SELECT a.date, s.roll_no, s.name AS student_name,
                   sub.code AS subject_code, sub.name AS subject_name, a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            JOIN subjects sub ON a.subject_id = sub.id
            WHERE a.date = ?
        """
        params = [date]
        if subject_id:
            query += " AND a.subject_id = ?"
            params.append(subject_id)
        query += " ORDER BY s.roll_no"
        records = conn.execute(query, params).fetchall()

    conn.close()
    return render_template(
        "datewise.html",
        records=records, date=date,
        subject_id=subject_id, subjects=subjects_list
    )


# ============================================================
# REPORT
# ============================================================
@app.route("/report")
def report():
    conn = get_db()
    subject_id = request.args.get("subject_id", "")
    subjects_list = conn.execute("SELECT * FROM subjects ORDER BY code").fetchall()

    query = """
        SELECT s.roll_no, s.name AS student_name,
               sub.code AS subject_code, sub.name AS subject_name,
               COUNT(a.id) AS total_classes,
               SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END) AS present_count,
               ROUND(100.0 * SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END) / COUNT(a.id), 2) AS percentage
        FROM students s
        JOIN attendance a ON s.id = a.student_id
        JOIN subjects sub ON a.subject_id = sub.id
    """
    params = []
    if subject_id:
        query += " WHERE a.subject_id = ?"
        params.append(subject_id)
    query += " GROUP BY s.id, sub.id ORDER BY s.roll_no, sub.code"

    report_data = conn.execute(query, params).fetchall()
    conn.close()
    return render_template(
        "report.html",
        report=report_data,
        subjects=subjects_list,
        subject_id=subject_id
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)