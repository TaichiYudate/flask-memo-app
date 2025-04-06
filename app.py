from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --- データベースの初期化 ---
def init_db():
    conn = sqlite3.connect("memos.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- トップページ ---
@app.route("/")
def index():
    return render_template("index.html")

# --- メモ追加ページ ---
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect("memos.db")
        c = conn.cursor()
        c.execute("INSERT INTO memos (title, content, category, created_at) VALUES (?, ?, ?, ?)",
                  (title, content, category, created_at))
        conn.commit()
        conn.close()
        return redirect(url_for("list_memos"))
    return render_template("add.html")

# --- メモ一覧ページ ---
@app.route("/list")
def list_memos():
    conn = sqlite3.connect("memos.db")
    c = conn.cursor()
    c.execute("SELECT * FROM memos ORDER BY created_at DESC")
    memos = c.fetchall()
    conn.close()
    return render_template("list.html", memos=memos)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

import os
print("📁 現在のテンプレートパス:", os.getcwd())
