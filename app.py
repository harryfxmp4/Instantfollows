```python
import os
import psycopg
from flask import Flask, render_template, request

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_conn():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")
    return psycopg.connect(DATABASE_URL)


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                followers INTEGER NOT NULL
            )
        """)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    username = request.form.get("username", "").strip()
    message = request.form.get("message", "").strip()
    followers = request.form.get("followers", "").strip()

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

    if followers < 1 or followers > 500:
        return render_template(
            "index.html",
            submitted=False
        )

    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO messages
            (username, message, followers)
            VALUES (%s, %s, %s)
            """,
            (username, message, followers)
        )

    return render_template(
        "index.html",
        submitted=True
    )


@app.route("/messages")
def view_messages():

    with get_conn() as conn:
        messages = conn.execute(
            """
            SELECT id, username, message, followers
            FROM messages
            ORDER BY id DESC
            """
        ).fetchall()

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
```
