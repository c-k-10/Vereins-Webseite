import sqlite3

connection = sqlite3.connect("projekt-verein.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS abteilungen (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")
connection.commit()

cursor.execute("INSERT INTO abteilungen (id, name) VALUES (?, ?)", (1, "Handball"))
cursor.execute("INSERT INTO abteilungen (id, name) VALUES (?, ?)", (2, "Fußball"))
cursor.execute("INSERT INTO abteilungen (id, name) VALUES (?, ?)", (3, "Tennis"))

connection.commit()

cursor.execute("SELECT * FROM abteilungen")
ergebnisse = cursor.fetchall()

for row in ergebnisse:
    print(row)

