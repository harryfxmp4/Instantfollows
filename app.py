from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = "messages.db"


def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            followers INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    username = request.form.get("username", "").strip()
    message = request.form.get("message", "").strip()
    followers = request.form.get("followers", "").strip()

    # Basic validation
    if not username or not message or not followers:
        return render_template(
            "index.html",
            submitted=False
        )

    try:
        followers = int(followers)
    except ValueError:
        return render_template(
            "index.html",
            submitted=False
        )

    # Keep followers within the demo limit
    if followers < 1 or followers > 500:
        return render_template(
            "index.html",
            submitted=False
        )

    # Save demo information
    conn = sqlite3.connect(DATABASE)

    conn.execute(
        """
        INSERT INTO messages
        (username, message, followers)
        VALUES (?, ?, ?)
        """,
        (username, message, followers)
    )

    conn.commit()
    conn.close()

    return render_template(
        "index.html",
        submitted=True
    )


@app.route("/messages")
def view_messages():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.execute(
        """
        SELECT id, username, message, followers
        FROM messages
        ORDER BY id DESC
        """
    )

    messages = cursor.fetchall()

    conn.close()

    return render_template(
        "messages.html",
        messages=messages
    )


init_db()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
