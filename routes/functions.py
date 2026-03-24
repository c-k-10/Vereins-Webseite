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

def get_fussball_table_data():
    conn = sqlite3.connect("projekt-verein.db")
    conn.row_factory = sqlite3.Row  # ermöglicht Zugriff per Spaltenname
    cur = conn.cursor()
    cur.execute("SELECT * FROM Fussball ORDER BY punkte DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_handball_table_data():
    conn = sqlite3.connect("projekt-verein.db")
    conn.row_factory = sqlite3.Row  # ermöglicht Zugriff per Spaltenname
    cur = conn.cursor()
    cur.execute("SELECT * FROM Handball ORDER BY punkte DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_tennis_table_data():
    conn = sqlite3.connect("projekt-verein.db")
    conn.row_factory = sqlite3.Row  # ermöglicht Zugriff per Spaltenname
    cur = conn.cursor()
    cur.execute("SELECT * FROM Handball ORDER BY punkte DESC")
    rows = cur.fetchall()
    conn.close()
    return rows