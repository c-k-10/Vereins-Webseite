from flask import Flask, request, render_template
import sqlite3
from flask import request, jsonify
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder=".")

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


bcrypt = Bcrypt()

def register_user():
    username = request.form.get("user-name")
    password = request.form.get("password")

    if not username or not password:
        return ({"error": "Username und Passwort erforderlich"})

    # Verbindung zur SQLite-Datenbank
    conn = sqlite3.connect("projekt-verein.db")
    cursor = conn.cursor()

    # Prüfen, ob Benutzername existiert
    cursor.execute("SELECT name FROM login WHERE name = ?", (username,))
    if cursor.fetchone() is not None:
        conn.close()
        return ({"error": "Benutzername existiert bereits"}),

    # Passwort hashen
    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    # Benutzer einfügen
    cursor.execute(
        "INSERT INTO login (name, passwort) VALUES (?, ?)",
        (username, pw_hash)
    )
    conn.commit()
    conn.close()

    return ({"message": "Account erfolgreich erstellt"})