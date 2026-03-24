from flask import Flask, request, render_template
import sqlite3
from routes.functions import check_login, get_table_data
from routes.route import app

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


@app.route("/pw_vergessen")
def pw_vergessen():
    return render_template("passwort_vergessen.html")

@app.route("/registrieren")
def registrieren():
    return render_template("registrierung.html")



if __name__ == "__main__":
    app.run(debug=True)