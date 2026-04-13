from flask import Flask, jsonify, redirect, request, render_template, session
import sqlite3
from routes.functions import check_login, get_fussball_table_data, get_handball_table_data, get_tennis_table_data, register_user, reset_password, get_user_profile, update_profile_picture
import os

DATABASE = os.path.join(os.path.dirname(__file__), "projekt-verein.db")
app = Flask(__name__, template_folder="templates")
app.secret_key = 'dein_geheimer_schluessel'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

#Route für die erste seite beim Aufruf vom Localhost (Der Login wird angezeigt)
@app.route("/")
def home():
    return render_template("login-2.html")

#Route für den Login
@app.route("/login2", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login-2.html")
    
    username = request.form.get("username")
    password = request.form.get("password")

    if check_login(username, password):
        session['username'] = username  
        return redirect("/index")  
    else:
        return render_template("login-2.html", error="Anmeldung fehlgeschlagen")
    
#Route für den Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/login2")

# ⭐ NEUE ROUTES: Profilbild-Verwaltung ⭐

#Route für Profil-Seite anzeigen
@app.route("/profil")
def profil():
    username = session.get('username')
    
    if not username:
        return redirect("/login2")
    
    # Verfügbare Profilbilder aus static/ laden
    profile_pictures = [
        'default_pb.png',
        'frosch_pb.png',
        'banane_pb.png',
        'mc_pb.png',
        'gatze_pb.png',
        'jonas_pb.png',
        'dominik_pb.png',
        'nils_pb.png'
    ]
    
    # Aktuelles Benutzer-Profil laden
    user = get_user_profile(username)
    current_picture = user['profilbild'] if user else 'default_pb.png'
    
    return render_template("profil.html", 
                         username=username, 
                         profile_pictures=profile_pictures,
                         current_picture=current_picture)

# API-Route: Profilbild aktualisieren
@app.route("/api/update-profile-picture", methods=["POST"])
def update_profile_picture_api():
    try:
        username = session.get('username')
        
        if not username:
            return jsonify({"success": False, "error": "Nicht eingeloggt"}), 401
        
        data = request.json
        new_picture = data.get('picture')
        
        if not new_picture:
            return jsonify({"success": False, "error": "Kein Bild ausgewählt"}), 400
        
        # Sicherheit: Nur erlaubte Bilder
        allowed_pictures = [
        'default_pb.png',
        'frosch_pb.png',
        'banane_pb.png',
        'mc_pb.png',
        'gatze_pb.png',
        'jonas_pb.png',
         'dominik_pb.png',
        'nils_pb.png'
        ]
        
        if new_picture not in allowed_pictures:
            return jsonify({"success": False, "error": "Ungültiges Bild"}), 400
        
        # Speichern in der Datenbank
        update_profile_picture(username, new_picture)
        
        return jsonify({"success": True, "picture": new_picture})
    
    except Exception as e:
        print(f"Fehler in update_profile_picture_api: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    
#Route für die Registrierung eines neuen Benutzers
@app.route("/new-user", methods=["GET", "POST"])
def new_user():
    if request.method == "GET":
        return render_template("registrierung.html")
    
#Route für idk grad xD
@app.route("/register", methods=["GET", "POST"])
def register_route():
    if request.method == "POST":
        return register_user()   
    return render_template("registrierung.html")  

#Route für die Passwortzurücksetzung
@app.route("/pwreset", methods=["GET", "POST"])
def pwreset_route():
    if request.method == "POST":
        return reset_password()
    return render_template("passwort_vergessen.html")




#=============================== REAKTIONEN ===============================

#Route für das Hinzufügen oder Entfernen von Reaktionen (Fussball)
@app.route("/fussball_add_reaction", methods=["POST"])
def fussball_add_reaction():
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
        c.execute("SELECT id FROM fussball_reaktionen WHERE id_spiel = ? AND user = ? AND reaktion = ?", (id_spiel, username, reaktion))
        existing = c.fetchone()

        if existing:
            # Entfernen (Toggle)
            c.execute("DELETE FROM fussball_reaktionen WHERE id_spiel = ? AND user = ? AND reaktion = ?", (id_spiel, username, reaktion))
        else:
            # Neue Reaktion hinzufügen
            c.execute("INSERT INTO fussball_reaktionen (id_spiel, reaktion, user) VALUES (?, ?, ?)", (id_spiel, reaktion, username))

        conn.commit()

        # Counts für alle Reaktionen dieses Spiels neu berechnen
        c.execute("""
            SELECT reaktion, COUNT(*) 
            FROM fussball_reaktionen 
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
    

#Route für das Hinzufügen oder Entfernen von Reaktionen (Handball)
@app.route("/handball_add_reaction", methods=["POST"])
def handball_add_reaction():
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
        c.execute("SELECT id FROM handball_reaktionen WHERE id_spiel = ? AND user = ? AND reaktion = ?", (id_spiel, username, reaktion))
        existing = c.fetchone()

        if existing:
            # Entfernen (Toggle)
            c.execute("DELETE FROM handball_reaktionen WHERE id_spiel = ? AND user = ? AND reaktion = ?", (id_spiel, username, reaktion))
        else:
            # Neue Reaktion hinzufügen
            c.execute("INSERT INTO handball_reaktionen (id_spiel, reaktion, user) VALUES (?, ?, ?)", (id_spiel, reaktion, username))

        conn.commit()

        # Counts für alle Reaktionen dieses Spiels neu berechnen
        c.execute("""
            SELECT reaktion, COUNT(*) 
            FROM handball_reaktionen 
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
    

#Route für das Hinzufügen oder Entfernen von Reaktionen (Tennis)
@app.route("/tennis_add_reaction", methods=["POST"])
def tennis_add_reaction():
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
        c.execute("SELECT id FROM tennis_reaktionen WHERE id_spiel = ? AND user = ? AND reaktion = ?", (id_spiel, username, reaktion))
        existing = c.fetchone()

        if existing:
            # Entfernen (Toggle)
            c.execute("DELETE FROM tennis_reaktionen WHERE id_spiel = ? AND user = ? AND reaktion = ?", (id_spiel, username, reaktion))
        else:
            # Neue Reaktion hinzufügen
            c.execute("INSERT INTO tennis_reaktionen (id_spiel, reaktion, user) VALUES (?, ?, ?)", (id_spiel, reaktion, username))

        conn.commit()

        # Counts für alle Reaktionen dieses Spiels neu berechnen
        c.execute("""
            SELECT reaktion, COUNT(*) 
            FROM tennis_reaktionen 
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

#==========================================================================





#Route für die Startseite
@app.route("/index")
def index():
    username = session.get('username')  # Username aus Session holen
    # Profilbild laden
    user_profile = get_user_profile(username) if username else None
    profile_picture = user_profile['profilbild'] if user_profile else 'default_pb.png'
    
    return render_template("index-2.html", username=username, profile_picture=profile_picture)

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
    return render_template("Werbung-2.html")


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
            FROM fussball_reaktionen
            WHERE id_spiel IN ({placeholders})
            GROUP BY id_spiel, reaktion
        """, all_spiele_ids).fetchall()
        for row in rows:
            if row['id_spiel'] not in reactions:
                reactions[row['id_spiel']] = {}
            reactions[row['id_spiel']][row['reaktion']] = row['count']

# ⭐ KOMMENTARE LADEN
    comments = {}
    if all_spiele_ids:
        placeholders = ','.join('?' for _ in all_spiele_ids)
        rows = conn.execute(f"""
            SELECT user_name, Kommentar, id_spiel
            FROM fussball_kommentare
            WHERE id_spiel IN ({placeholders})
            ORDER BY id DESC
        """, all_spiele_ids).fetchall()

        for row in rows:
            comments.setdefault(row["id_spiel"], []).append({
                "user": row["user_name"],
                "text": row["Kommentar"]
            })

    conn.close()
    
    # Profilbild laden
    user_profile = get_user_profile(username) if username else None
    profile_picture = user_profile['profilbild'] if user_profile else 'default_pb.png'

    return render_template(
        "fussball-2.html",
        data=data,
        letzte_spiele=letzte_spiele,
        naechste_spiele=naechste_spiele,
        reactions=reactions,
        comments=comments,
        username=username,
        profile_picture=profile_picture
    )


@app.route("/handball")
def handball():
    username = session.get('username')  # Username aus Session holen
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

    # Reaction-Counts für alle Spiele laden
    all_spiele_ids = [spiel['id'] for spiel in letzte_spiele] + [spiel['id'] for spiel in naechste_spiele]
    reactions = {}
    if all_spiele_ids:
        placeholders = ','.join('?' for _ in all_spiele_ids)
        rows = conn.execute(f"""
            SELECT id_spiel, reaktion, COUNT(*) as count
            FROM handball_reaktionen
            WHERE id_spiel IN ({placeholders})
            GROUP BY id_spiel, reaktion
        """, all_spiele_ids).fetchall()
        for row in rows:
            if row['id_spiel'] not in reactions:
                reactions[row['id_spiel']] = {}
            reactions[row['id_spiel']][row['reaktion']] = row['count']

# ⭐ KOMMENTARE LADEN
    comments = {}
    if all_spiele_ids:
        placeholders = ','.join('?' for _ in all_spiele_ids)
        rows = conn.execute(f"""
            SELECT user_name, Kommentar, id_spiel
            FROM handball_kommentare
            WHERE id_spiel IN ({placeholders})
            ORDER BY id DESC
        """, all_spiele_ids).fetchall()

        for row in rows:
            comments.setdefault(row["id_spiel"], []).append({
                "user": row["user_name"],
                "text": row["Kommentar"]
            })

    conn.close()
    
    # Profilbild laden
    user_profile = get_user_profile(username) if username else None
    profile_picture = user_profile['profilbild'] if user_profile else 'default_pb.png'

    return render_template(
        "handball-2.html",
        data=data,
        letzte_spiele=letzte_spiele,
        naechste_spiele=naechste_spiele,
        reactions=reactions,
        comments=comments,
        username=username,
        profile_picture=profile_picture
    )

@app.route("/tennis")
def tennis():
    username = session.get('username')  # Username aus Session holen
    # Tabelle laden (so wie bei dir)
    data = get_tennis_table_data()

    # Verbindung öffnen
    conn = get_db_connection()

    # LETZTE SPIELE (Datum <= heute)
    letzte_spiele = conn.execute("""
        SELECT id, heimverein, gastverein, datum, uhrzeit, "heim-tore", "gast-tore"
        FROM tennis_spiele
        WHERE datum <= DATE('now')
        ORDER BY datum DESC
        LIMIT 5;
    """).fetchall()

    # NÄCHSTE SPIELE (Datum > heute)
    naechste_spiele = conn.execute("""
        SELECT id, heimverein, gastverein, datum, uhrzeit
        FROM tennis_spiele
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
            FROM tennis_reaktionen
            WHERE id_spiel IN ({placeholders})
            GROUP BY id_spiel, reaktion
        """, all_spiele_ids).fetchall()
        for row in rows:
            if row['id_spiel'] not in reactions:
                reactions[row['id_spiel']] = {}
            reactions[row['id_spiel']][row['reaktion']] = row['count']

# ⭐ KOMMENTARE LADEN
    comments = {}
    if all_spiele_ids:
        placeholders = ','.join('?' for _ in all_spiele_ids)
        rows = conn.execute(f"""
            SELECT user_name, Kommentar, id_spiel
            FROM tennis_kommentare
            WHERE id_spiel IN ({placeholders})
            ORDER BY id DESC
        """, all_spiele_ids).fetchall()

        for row in rows:
            comments.setdefault(row["id_spiel"], []).append({
                "user": row["user_name"],
                "text": row["Kommentar"]
            })

    conn.close()
    
    # Profilbild laden
    user_profile = get_user_profile(username) if username else None
    profile_picture = user_profile['profilbild'] if user_profile else 'default_pb.png'

    return render_template(
        "tennis-2.html",
        data=data,
        letzte_spiele=letzte_spiele,
        naechste_spiele=naechste_spiele,
        reactions=reactions,
        comments=comments,
        username=username,
        profile_picture=profile_picture
    )

@app.route("/pw_vergessen")
def pw_vergessen():
    return render_template("passwort_vergessen.html")

@app.route("/registrieren")
def registrieren():
    return render_template("registrierung.html")

@app.route("/joke")
def joke():
    return render_template("joke.html")





#Routen für das Hinzufügen von Kommentaren (je Sportart)
@app.post("/fussball_add_comment")
def fussball_add_comment():
    data = request.get_json()
    spiel_id = data["spiel_id"]
    text = data["text"]

    # Username aus Session holen
    username = session.get("username", "Unbekannt")

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO fussball_kommentare (user_name, Kommentar, id_spiel) VALUES (?, ?, ?)",
        (username, text, spiel_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "user": username})

@app.post("/handball_add_comment")
def handball_add_comment():
    data = request.get_json()
    spiel_id = data["spiel_id"]
    text = data["text"]

    # Username aus Session holen
    username = session.get("username", "Unbekannt")

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO handball_kommentare (user_name, Kommentar, id_spiel) VALUES (?, ?, ?)",
        (username, text, spiel_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "user": username})

@app.post("/tennis_add_comment")
def tennis_add_comment():
    data = request.get_json()
    spiel_id = data["spiel_id"]
    text = data["text"]

    # Username aus Session holen
    username = session.get("username", "Unbekannt")

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO tennis_kommentare (user_name, Kommentar, id_spiel) VALUES (?, ?, ?)",
        (username, text, spiel_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "user": username})




if __name__ == "__main__":
    app.run(debug=True)