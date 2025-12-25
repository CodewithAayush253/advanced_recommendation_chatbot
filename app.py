from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

recommendations = {
    "Action": {
        "movies": ["John Wick", "Avengers", "Mad Max"],
        "books": ["The Bourne Identity", "Hunger Games"]
    },
    "Romance": {
        "movies": ["Titanic", "The Notebook"],
        "books": ["Me Before You", "Pride and Prejudice"]
    },
    "Sci-Fi": {
        "movies": ["Interstellar", "Inception"],
        "books": ["Dune", "The Time Machine"]
    },
    "Motivation": {
        "movies": ["The Pursuit of Happyness", "Rocky"],
        "books": ["Atomic Habits", "Think and Grow Rich"]
    }
}

def save_user(name, genre):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, genre) VALUES (?,?)", (name, genre))
    conn.commit()
    conn.close()

def get_user_history(name):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT genre FROM users WHERE name=?", (name,))
    data = cursor.fetchall()
    conn.close()
    return [i[0] for i in data]

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    history = []

    if request.method == "POST":
        name = request.form["name"]
        genre = request.form["genre"]

        save_user(name, genre)
        history = get_user_history(name)
        result = recommendations.get(genre)

    return render_template("index.html", result=result, history=history)

if __name__ == "__main__":
    app.run(debug=True)
