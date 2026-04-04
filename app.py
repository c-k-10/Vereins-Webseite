from flask import Flask, jsonify, redirect, request, render_template, session
import sqlite3
from routes.functions import check_login, get_fussball_table_data, get_handball_table_data, get_tennis_table_data, register_user, reset_password
import os

DATABASE = os.path.join(os.path.dirname(__file__), "projekt-verein.db")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__, template_folder="templates")
app.secret_key = 'dein_geheimer_schluessel'

@app.route("/login2", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login-2.html")
    
    username = request.form.get("username")
    password = request.form.get("password")

    if check_login(username, password):
        session['username'] = username  # Username in Session speichern
        return redirect("/index")  # Nach Login zur Index-Seite leiten
    else:
        return render_template("login-2.html", error="Anmeldung fehlgeschlagen")
    

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/login2")
    
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

@app.route("/add_reaction", methods=["POST"])
def add_reaction():
    print("Route erreicht")
    try:
        data = request.json
        print(f"Data: {data}")
        id_spiel = data["id_spiel"]
        reaktion = data["reaktion"]
        username = session.get('username')  # Username aus Session holen

        if not username:
            return jsonify({"error": "Nicht eingeloggt"}), 401  # Fehler, wenn nicht eingeloggt

        conn = get_db_connection()
        c = conn.cursor()

        # Prüfen, ob User schon diese Reaktion für dieses Spiel hat
        c.execute("SELECT id FROM reaktionen WHERE id_spiel = ? AND user = ? AND reaktion = ?", (id_spiel, username, reaktion))
        existing = c.fetchone()

        if existing:
            # Entfernen (Toggle)
            c.execute("DELETE FROM reaktionen WHERE id_spiel = ? AND user = ? AND reaktion = ?", (id_spiel, username, reaktion))
        else:
            # Neue Reaktion hinzufügen
            c.execute("INSERT INTO reaktionen (id_spiel, reaktion, user) VALUES (?, ?, ?)", (id_spiel, reaktion, username))

        conn.commit()

        # Counts für alle Reaktionen dieses Spiels neu berechnen
        c.execute("""
            SELECT reaktion, COUNT(*) 
            FROM reaktionen 
            WHERE id_spiel = ?
            GROUP BY reaktion
        """, (id_spiel,))

        result = {row[0]: row[1] for row in c.fetchall()}
        print(f"Result: {result}")

        conn.close()
        return jsonify(result)
    except Exception as e:
        print(f"Fehler: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route("/")
def home():
    return render_template("login-2.html")

@app.route("/index")
def index():
    username = session.get('username')  # Username aus Session holen
    return render_template("index-2.html", username=username)

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
    username = session.get('username')  # Username aus Session holen
    # Tabelle laden (so wie bei dir)
    data = get_fussball_table_data()

    # Verbindung öffnen
    conn = get_db_connection()

    # LETZTE SPIELE (Datum <= heute)
    letzte_spiele = conn.execute("""
        SELECT id, heimverein, gastverein, datum, uhrzeit, "heim-tore", "gast-tore"
        FROM fussball_spiele
        WHERE datum <= DATE('now')
        ORDER BY datum DESC
        LIMIT 5;
    """).fetchall()

    # NÄCHSTE SPIELE (Datum > heute)
    naechste_spiele = conn.execute("""
        SELECT id, heimverein, gastverein, datum, uhrzeit
        FROM fussball_spiele
        WHERE datum > DATE('now')
        ORDER BY datum ASC
        LIMIT 5;
    """).fetchall()

    # Reaction-Counts für alle Spiele laden
    all_spiele_ids = [spiel['id'] for spiel in letzte_spiele] + [spiel['id'] for spiel in naechste_spiele]
    reactions = {}
    if all_spiele_ids:
        placeholders = ','.join('?' for _ in all_spiele_ids)
        rows = conn.execute(f"""
            SELECT id_spiel, reaktion, COUNT(*) as count
            FROM reaktionen
            WHERE id_spiel IN ({placeholders})
            GROUP BY id_spiel, reaktion
        """, all_spiele_ids).fetchall()
        for row in rows:
            if row['id_spiel'] not in reactions:
                reactions[row['id_spiel']] = {}
            reactions[row['id_spiel']][row['reaktion']] = row['count']

    conn.close()

    return render_template(
        "fussball-2.html",
        data=data,
        letzte_spiele=letzte_spiele,
        naechste_spiele=naechste_spiele,
        reactions=reactions,
        username=username
    )


@app.route("/handball")
def handball():
    # Tabelle laden (so wie bei dir)
    data = get_handball_table_data()

    # Verbindung öffnen
    conn = get_db_connection()

    # LETZTE SPIELE (Datum <= heute)
    letzte_spiele = conn.execute("""
        SELECT id, heimverein, gastverein, datum, uhrzeit, "heim-tore", "gast-tore"
        FROM handball_spiele
        WHERE datum <= DATE('now')
        ORDER BY datum DESC
        LIMIT 5;
    """).fetchall()

    # NÄCHSTE SPIELE (Datum > heute)
    naechste_spiele = conn.execute("""
        SELECT id, heimverein, gastverein, datum, uhrzeit
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