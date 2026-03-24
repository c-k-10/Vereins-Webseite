from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__, template_folder=".")

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
    return render_template("fussball.html")

@app.route("/handball")
def handball():
    return render_template("handball.html")

@app.route("/tennis")
def tennis():
    return render_template("tennis.html")
