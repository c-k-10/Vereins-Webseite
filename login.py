from flask import Flask, request, render_template
import sqlite3
import route 

app = Flask(__name__, template_folder=".")

@app.route("/")
def home():
    return render_template("login-2.html")

@app.route("/index")
def index():
    return render_template("index-2.html")

@app.route("/news_tennis")
def news_tennis():
    return render_template("news_tennis.html")

@app.route("/news_handball")
def news_handball():
    return render_template("news_handball.html")

@app.route("/news_fussball")
def news_fussball():
    return render_template("news-fussball-2.html")

@app.route("/fussball")
def fussball():
    data = get_table_data()
    return render_template("fussball-2.html", data=data)

@app.route("/handball")
def handball():
    return render_template("handball.html")

@app.route("/tennis")
def tennis():
    return render_template("tennis.html")


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


def get_table_data():
    conn = sqlite3.connect("projekt-verein.db")
    conn.row_factory = sqlite3.Row  # ermöglicht Zugriff per Spaltenname
    cur = conn.cursor()
    cur.execute("SELECT * FROM Fussball ORDER BY punkte DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

    


@app.route("/login2", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login-2.html")
    
    username = request.form.get("username")
    password = request.form.get("password")

    if check_login(username, password):
        return render_template("index-2.html", username=username)
    else:
        return render_template("login-2.html", error="Anmeldung fehlgeschlagen")
  

if __name__ == "__main__":
    app.run(debug=True)