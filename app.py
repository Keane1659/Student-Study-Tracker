import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "assignments.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            class_name TEXT NOT NULL,
            due_date TEXT NOT NULL,
            estimated_hours REAL DEFAULT 0,
            completed INTEGER DEFAULT 0
        )"""
    )
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM assignments ORDER BY completed, due_date"
    ).fetchall()
    conn.close()
    return render_template("index.html", assignments=rows)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    class_name = request.form.get("class_name", "").strip()
    due_date = request.form.get("due_date", "").strip()
    try:
        hours = float(request.form.get("estimated_hours") or 0)
    except ValueError:
        hours = 0
    if title and class_name and due_date:
        conn = get_db()
        conn.execute(
            "INSERT INTO assignments (title, class_name, due_date, estimated_hours) VALUES (?, ?, ?, ?)",
            (title, class_name, due_date, hours),
        )
        conn.commit()
        conn.close()
    return redirect(url_for("index"))


@app.route("/toggle/<int:assignment_id>", methods=["POST"])
def toggle(assignment_id):
    conn = get_db()
    conn.execute(
        "UPDATE assignments SET completed = 1 - completed WHERE id = ?",
        (assignment_id,),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:assignment_id>", methods=["POST"])
def delete(assignment_id):
    conn = get_db()
    conn.execute("DELETE FROM assignments WHERE id = ?", (assignment_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))