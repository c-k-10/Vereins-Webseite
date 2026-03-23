from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__, template_folder=".")


def check_login(username, password):
    # Verbindung zur SQLite-Datenbank
    conn = sqlite3.connect("projekt-verein.db")
    cursor = conn.cursor()

    # Benutzer suchen
    cursor.execute("SELECT passwort FROM login WHERE name = ?", (username,))
    result = cursor.fetchone()

    conn.close()

    # Prüfen, ob Benutzer existiert und Passwort stimmt
    if result is None:
        return False  # Benutzer nicht gefunden

    stored_password = result[0]
    return stored_password == password


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form.get("username")
    password = request.form.get("password")

    if check_login(username, password):
        return render_template("index.html")
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)