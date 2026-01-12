import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_PATH = Path(__file__).with_name("movies.db")


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year TEXT NOT NULL,
            actors TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


# ważne: init_db wykona się automatycznie zanim poleci pierwszy request
_db_initialized = False


@app.before_request
def ensure_db():
    global _db_initialized
    if not _db_initialized:
        init_db()
        _db_initialized = True


def fetch_movies() -> list[tuple]:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, year, actors FROM movies ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [(r["id"], r["title"], r["year"], r["actors"]) for r in rows]


# usuwanie filmów po ID (bezpieczne placeholdery)
def delete_movies_by_ids(ids: list[int]) -> None:
    if not ids:
        return

    placeholders = ",".join(["?"] * len(ids))  # np. "?, ?, ?"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM movies WHERE id IN ({placeholders})", ids)
    conn.commit()
    conn.close()


# endpoint "/" obsługuje też POST (usuwanie)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # pobranie listy zaznaczonych checkboxów
        movies_to_remove_ids = request.form.getlist("movieToRemove")

        # checkboxy zwracają stringi -> konwersja na int
        if movies_to_remove_ids:
            ids_int = []
            for x in movies_to_remove_ids:
                try:
                    ids_int.append(int(x))
                except ValueError:
                    # w przypadku podmiany ignorowanie śmieci
                    pass

            delete_movies_by_ids(ids_int)

        # PRG: po usunięciu powrót na GET /
        return redirect(url_for("home"))

    movies = fetch_movies()
    return render_template("home.html", movies=movies)


@app.route("/addMovie", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        movie_title = request.form.get("title", "").strip()
        movie_year = request.form.get("year", "").strip()
        movie_actors = request.form.get("actors", "").strip()

        if movie_title and movie_year and movie_actors:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO movies (title, year, actors) VALUES (?, ?, ?)",
                (movie_title, movie_year, movie_actors),
            )
            conn.commit()
            conn.close()

        return redirect(url_for("home"))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)