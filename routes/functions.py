from flask import Flask, request, render_template
import sqlite3
from flask import request, jsonify
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder=".")
bcrypt = Bcrypt()

def init_db():
    """Initialisiert die Datenbank und fügt Spalten hinzu wenn nötig"""
    try:
        conn = sqlite3.connect("projekt-verein.db")
        cursor = conn.cursor()
        
        # Überprüfe ob profilbild Spalte existiert
        cursor.execute("PRAGMA table_info(login)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'profilbild' not in columns:
            print("🔧 Migrating: Adding 'profilbild' column to login table...")
            # Spalte hinzufügen mit Default-Wert
            cursor.execute("""
                ALTER TABLE login 
                ADD COLUMN profilbild TEXT DEFAULT 'default_pb.png'
            """)
            conn.commit()
            print("✅ Migration successful!")
        else:
            print("✅ 'profilbild' column already exists")
        
        conn.close()
    except Exception as e:
        print(f"❌ Database migration error: {e}")

init_db()

def check_login(username, password):
    conn = sqlite3.connect("projekt-verein.db")
    cursor = conn.cursor()

    cursor.execute("SELECT passwort FROM login WHERE name = ?", (username,))
    result = cursor.fetchone()

    conn.close()

    if result is None:
        return False

    stored_hash = result[0]
    return bcrypt.check_password_hash(stored_hash, password)

def get_fussball_table_data():
    conn = sqlite3.connect("projekt-verein.db")
    conn.row_factory = sqlite3.Row  # ermöglicht Zugriff per Spaltenname
    cur = conn.cursor()
    cur.execute("SELECT * FROM Fussball ORDER BY gewonnen DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_handball_table_data():
    conn = sqlite3.connect("projekt-verein.db")
    conn.row_factory = sqlite3.Row  # ermöglicht Zugriff per Spaltenname
    cur = conn.cursor()
    cur.execute("SELECT * FROM handball ORDER BY gewonnen DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_tennis_table_data():
    conn = sqlite3.connect("projekt-verein.db")
    conn.row_factory = sqlite3.Row  # ermöglicht Zugriff per Spaltenname
    cur = conn.cursor()
    cur.execute("SELECT * FROM tennis ORDER BY gewonnen DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def register_user():
    username = request.form.get("user-name")
    password = request.form.get("password")
    password2 = request.form.get("password2")   # zweites Passwortfeld

    # 1. Felder prüfen
    if not username or not password or not password2:
        return render_template("registrierung.html", error="Bitte alle Felder ausfüllen")

    # 2. Passwörter vergleichen
    if password != password2:
        return render_template("registrierung.html", error="Die Passwörter stimmen nicht überein")

    # 3. DB-Verbindung
    conn = sqlite3.connect("projekt-verein.db")
    cursor = conn.cursor()

    # 4. Prüfen, ob Benutzer existiert
    cursor.execute("SELECT name FROM login WHERE name = ?", (username,))
    if cursor.fetchone() is not None:
        conn.close()
        return render_template("registrierung.html", error="Benutzername existiert bereits")

    # 5. Passwort hashen
    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    # 6. Einfügen (mit Default-Profilbild)
    cursor.execute(
        "INSERT INTO login (name, passwort, profilbild) VALUES (?, ?, ?)",
        (username, pw_hash, 'default_pb.png')
    )
    conn.commit()
    conn.close()

    # 7. Weiterleitung nach erfolgreicher Registrierung
    return render_template("login-2.html", message="Registrierung erfolgreich!")

def reset_password():

    username = request.form.get("user-name")
    new_password = request.form.get("password")
    new_password2 = request.form.get("password2")

    # 1. Felder prüfen
    if not username or not new_password or not new_password2:
        return render_template("passwort_vergessen.html", error="Bitte alle Felder ausfüllen")

    # 2. Passwörter vergleichen
    if new_password != new_password2:
        return render_template("passwort_vergessen.html", error="Die Passwörter stimmen nicht überein")

    # 3. DB-Verbindung
    conn = sqlite3.connect("projekt-verein.db")
    cursor = conn.cursor()

    # 4. Prüfen, ob Benutzer existiert
    cursor.execute("SELECT name FROM login WHERE name = ?", (username,))
    if cursor.fetchone() is None:
        conn.close()
        return render_template("passwort_vergessen.html", error="Benutzer wurde nicht gefunden")

    # 5. Neues Passwort hashen
    pw_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")

    # 6. Passwort aktualisieren
    cursor.execute(
        "UPDATE login SET passwort = ? WHERE name = ?",
        (pw_hash, username)
    )
    conn.commit()
    conn.close()

    # 7. Weiterleitung zum Login
    return render_template("login-2.html", message="Passwort erfolgreich zurückgesetzt!")

def get_user_profile(username):
    """Laden des Benutzer-Profils mit Profilbild"""
    conn = sqlite3.connect("projekt-verein.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, profilbild FROM login WHERE name = ?", (username,))
    user = cursor.fetchone()
    
    conn.close()
    return user

def update_profile_picture(username, new_picture):
    """Aktualisiert das Profilbild eines Benutzers"""
    try:
        conn = sqlite3.connect("projekt-verein.db")
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE login SET profilbild = ? WHERE name = ?",
            (new_picture, username)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Fehler beim Update des Profilbilds: {e}")
        raise