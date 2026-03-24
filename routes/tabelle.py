import sqlite3

connection = sqlite3.connect("projekt-verein.db")
cursor = connection.cursor()

#Tabelle Login
cursor.execute("""
CREATE TABLE IF NOT EXISTS login (
    id INTEGER PRIMARY KEY,
    name TEXT,
    passwort TEXT
)
""")
connection.commit()

cursor.execute("SELECT COUNT(*) FROM login")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO login (id, name, passwort) VALUES (?, ?, ?)", (1, "pavitheking", "passwort"))
    cursor.execute("INSERT INTO login (id, name, passwort) VALUES (?, ?, ?)", (2, "c_k_10", "passwort"))

connection.commit()

#Tabelle Spiele
cursor.execute("""
CREATE TABLE IF NOT EXISTS spiele (
    id INTEGER PRIMARY KEY,
    heimverein TEXT,
    gastverein TEXT,
    datum DATE,
    uhrzeit TEXT,
    'heim-tore' INTEGER,
    'gast-tore' INTEGER
)
""")
connection.commit()

cursor.execute("SELECT COUNT(*) FROM spiele")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO spiele (id, heimverein, gastverein, datum, uhrzeit,'heim-tore', 'gast-tore') VALUES (?, ?, ?, ?, ?, ?, ?)", (1, "TSH Herzogenaurach", "FC Rasenmäher", '2026-01-20', "16:00", 30, 28 ))
    
connection.commit()

#Tabelle Handball
cursor.execute("""
CREATE TABLE IF NOT EXISTS handball (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verein TEXT,
    spiele INTEGER,
    gewonnen INTEGER,
    unentschieden INTEGER,
    verloren INTEGER,
    punkte TEXT
  
)
""")
connection.commit()

cursor.execute("SELECT COUNT(*) FROM handball")

if cursor.fetchone()[0] == 0:

   cursor.execute("INSERT INTO handball (id, verein, spiele, gewonnen, unentschieden, verloren, punkte) VALUES (?, ?, ?, ?, ?, ?, ?)", (1, "TSH Herzogenaurach", 5, 3, 1, 1, "17:3"))
   cursor.execute("INSERT INTO handball (id, verein, spiele, gewonnen, unentschieden, verloren, punkte) VALUES (?, ?, ?, ?, ?, ?, ?)", (2, "FC Rasenmäher", 5, 2, 1, 2, "14:3"))
   cursor.execute("INSERT INTO handball (id, verein, spiele, gewonnen, unentschieden, verloren, punkte) VALUES (?, ?, ?, ?, ?, ?, ?)", (3, "TSV Röttenbach", 5, 1, 1, 3, "10:3"))
   cursor.execute("INSERT INTO handball (id, verein, spiele, gewonnen, unentschieden, verloren, punkte) VALUES (?, ?, ?, ?, ?, ?, ?)", (4, "TSV Altenberg", 5, 0, 1, 4, "3:17"))
connection.commit()

#Tabelle Fussball
cursor.execute("""
CREATE TABLE IF NOT EXISTS Fussball (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verein TEXT,
    spiele INTEGER,
    gewonnen INTEGER,
    unentschieden INTEGER,
    verloren INTEGER,
    punkte TEXT

)
""")
connection.commit()

cursor.execute("SELECT COUNT(*) FROM Fussball")

if cursor.fetchone()[0] == 0:

   cursor.execute("INSERT INTO Fussball (id, verein, spiele, gewonnen, unentschieden, verloren, punkte) VALUES (?, ?, ?, ?, ?, ?, ?)", (1, "TSH Herzogenaurach", 5, 3, 1, 1, "17:3"))
   cursor.execute("INSERT INTO Fussball (id, verein, spiele, gewonnen, unentschieden, verloren, punkte) VALUES (?, ?, ?, ?, ?, ?, ?)", (2, "FC Rasenmäher", 5, 2, 1, 2, "14:3"))
   cursor.execute("INSERT INTO Fussball (id, verein, spiele, gewonnen, unentschieden, verloren, punkte) VALUES (?, ?, ?, ?, ?, ?, ?)", (3, "TSV Röttenbach", 5, 1, 1, 3, "10:3"))
   cursor.execute("INSERT INTO Fussball (id, verein, spiele, gewonnen, unentschieden, verloren, punkte) VALUES (?, ?, ?, ?, ?, ?, ?)", (4, "TSV Altenberg", 5, 0, 1, 4, "3:17"))
connection.commit()

#Tabelle Tennis
cursor.execute("""
CREATE TABLE IF NOT EXISTS tennis (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
    verein TEXT,
    spiele INTEGER,
    gewonnen INTEGER,
    unentschieden INTEGER,
    verloren INTEGER,
    punkte TEXT
)
""")
connection.commit()

cursor.execute("SELECT COUNT(*) FROM tennis")

if cursor.fetchone()[0] == 0:

   cursor.execute(
    "INSERT INTO tennis (id, verein, spiele, gewonnen, unentschieden, verloren, punkte) VALUES (?, ?, ?, ?, ?, ?, ?)", (1, "TS Herzo", 5, 3, 1, 1, "17:3")
)
 
#Tabelle Kommentare 
cursor.execute("""
CREATE TABLE IF NOT EXISTS kommentare (
    id INTEGER PRIMARY KEY,
    user_name TEXT,
    Kommentar TEXT
)
""")
connection.commit()

cursor.execute("SELECT COUNT(*) FROM kommentare")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO kommentare (id, user_name, Kommentar) VALUES (?, ?, ?)", (1, "pavitheking", "Das ist der erste Kommentar."))
    cursor.execute("INSERT INTO kommentare (id, user_name, Kommentar) VALUES (?, ?, ?)", (2, "c_k_10", "HDF @pavitheking"))
connection.commit()

#Tabelle Reaktionen 
cursor.execute("""
CREATE TABLE IF NOT EXISTS reaktionen (
    id_kommentar INTEGER PRIMARY KEY,
    reaktion TEXT
)
""")
connection.commit()

cursor.execute("SELECT COUNT(*) FROM reaktionen")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO reaktionen (id_kommentar, reaktion) VALUES (?, ?)", (1, "Super"))
    cursor.execute("INSERT INTO reaktionen (id_kommentar, reaktion) VALUES (?, ?)", (2, "Klasse"))
connection.commit()