from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import requests
import os

app = Flask(__name__, static_folder='statics', template_folder='templates')

DB_PATH = "db/habits.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

QUOTE_API_URL = "https://zenquotes.io/api/random"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            frequency TEXT NOT NULL,
            streak INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Fetch quote from API
def fetch_quote():
    try:
        res = requests.get(QUOTE_API_URL, timeout=5)
        res.raise_for_status()
        data = res.json()
        if isinstance(data, list) and len(data) > 0:
            return data[0]['q'], data[0]['a']
    except:
        pass
    return "Stay consistent!", "Habit Tracker"

@app.route("/")
def index():
    quote, author = fetch_quote()
    return render_template("index.html", quote=quote, author=author)

# API route for JS quote fetch
@app.route("/api/quote")
def get_quote():
    quote, author = fetch_quote()
    return jsonify({"quote": quote, "author": author})


# API routes for habits
@app.route("/api/habits", methods=["GET", "POST", "PUT", "DELETE"])
def habits():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if request.method == "GET":
        c.execute("SELECT * FROM habits")
        rows = c.fetchall()
        habits_list = [{"id": r[0], "name": r[1], "frequency": r[2], "streak": r[3]} for r in rows]
        conn.close()
        return jsonify(habits_list)

    data = request.get_json()

    if request.method == "POST":
        c.execute("INSERT INTO habits (name, frequency) VALUES (?,?)", (data["name"], data["frequency"]))
        conn.commit()
        conn.close()
        return jsonify({"status": "Habit added"}), 201

    if request.method == "PUT":
        c.execute(
            "UPDATE habits SET name=?, frequency=?, streak=? WHERE id=?",
            (data["name"], data["frequency"], data["streak"], data["id"])
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "Habit updated"})

    if request.method == "DELETE":
        c.execute("DELETE FROM habits WHERE id=?", (data["id"],))
        conn.commit()
        conn.close()
        return jsonify({"status": "Habit deleted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
input("Press Enter to exit...")