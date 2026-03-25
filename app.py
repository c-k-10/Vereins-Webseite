from flask import Flask, request, render_template
import sqlite3
from routes.functions import check_login, get_fussball_table_data, get_handball_table_data, get_tennis_table_data, register_user

DATABASE = "projekt-verein.db"

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
    

@app.post("/register")
def register_route():
    if register_user():
        return render_template("login-2.html", message="Account erfolgreich erstellt")
    else:        
        return render_template("registrierung.html", error="Benutzername existiert bereits")
    

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

@app.route("/fussball")
def fussball():
    data = get_fussball_table_data()
    return render_template("fussball-2.html", data=data)

@app.route("/handball")
def handball():
    data = get_handball_table_data()
    return render_template("handball-2.html", data=data)

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



if __name__ == "__main__":
    app.run(debug=True)