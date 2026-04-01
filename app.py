from flask import Flask, redirect, request, render_template
import sqlite3
from routes.functions import check_login, get_fussball_table_data, get_handball_table_data, get_tennis_table_data, register_user, reset_password

DATABASE = "projekt-verein.db"


def get_db_connection():
    conn = sqlite3.connect("projekt-verein.db")
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__, template_folder="templates")

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
    
@app.route("/new-user", methods=["GET", "POST"])
def new_user():
    if request.method == "GET":
        return render_template("registrierung.html")
    

@app.route("/register", methods=["GET", "POST"])
def register_route():
    if request.method == "POST":
        return register_user()   # WICHTIG: Immer return!
    return render_template("registrierung.html")  # GET-Aufruf


@app.route("/pwreset", methods=["GET", "POST"])
def pwreset_route():
    if request.method == "POST":
        return reset_password()
    return render_template("passwort_vergessen.html")



# @app.post("/kommentar_hinzufuegen")
# def kommentar_hinzufuegen():
#     spiel_id = request.form["spiel_id"]
#     text = request.form["kommentar"]

#     db.execute(
#         "INSERT INTO kommentare (spiel_id, user, text) VALUES (?, ?, ?)",
#         (spiel_id, "Fan", text)
#     )
#     db.commit()

#     return redirect(request.referrer)
    

    

@app.route("/")
def home():
    return render_template("login-2.html")

@app.route("/index")
def index():
    return render_template("index-2.html")

@app.route("/news_tennis")
def news_tennis():
    return render_template("news_tennis-2.html")

@app.route("/news_handball")
def news_handball():
    return render_template("news_handball-2.html")

@app.route("/news_fussball")
def news_fussball():
    return render_template("news-fussball-2.html")

@app.route("/Werbung")
def news_Werbung():
    return render_template("Werbung.html")

@app.route("/fussball")
def fussball():
        # Tabelle laden (so wie bei dir)
    data = get_fussball_table_data()

    # Verbindung öffnen
    conn = get_db_connection()

    # LETZTE SPIELE (Datum <= heute)
    letzte_spiele = conn.execute("""
        SELECT heimverein, gastverein, datum, uhrzeit, "heim-tore", "gast-tore"
        FROM fussball_spiele
        WHERE datum <= DATE('now')
        ORDER BY datum DESC
        LIMIT 5;
    """).fetchall()

    # NÄCHSTE SPIELE (Datum > heute)
    naechste_spiele = conn.execute("""
        SELECT heimverein, gastverein, datum, uhrzeit
        FROM fussball_spiele
        WHERE datum > DATE('now')
        ORDER BY datum ASC
        LIMIT 5;
    """).fetchall()

    conn.close()

    return render_template(
        "fussball-2.html",
        data=data,
        letzte_spiele=letzte_spiele,
        naechste_spiele=naechste_spiele
    )

@app.route("/handball")
def handball():
           # Tabelle laden (so wie bei dir)
    data = get_handball_table_data()

    # Verbindung öffnen
    conn = get_db_connection()

    # LETZTE SPIELE (Datum <= heute)
    letzte_spiele = conn.execute("""
        SELECT heimverein, gastverein, datum, uhrzeit, "heim-tore", "gast-tore"
        FROM handball_spiele
        WHERE datum <= DATE('now')
        ORDER BY datum DESC
        LIMIT 5;
    """).fetchall()

    # NÄCHSTE SPIELE (Datum > heute)
    naechste_spiele = conn.execute("""
        SELECT heimverein, gastverein, datum, uhrzeit
        FROM handball_spiele
        WHERE datum > DATE('now')
        ORDER BY datum ASC
        LIMIT 5;
    """).fetchall()

    conn.close()

    return render_template(
        "handball-2.html",
        data=data,
        letzte_spiele=letzte_spiele,
        naechste_spiele=naechste_spiele
    )

@app.route("/tennis")
def tennis():
    data = get_tennis_table_data()
    return render_template("tennis-2.html", data=data)

@app.route("/pw_vergessen")
def pw_vergessen():
    return render_template("passwort_vergessen.html")

@app.route("/registrieren")
def registrieren():
    return render_template("registrierung.html")

@app.route("/joke")
def joke():
    return render_template("joke.html")



if __name__ == "__main__":
    app.run(debug=True)