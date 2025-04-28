from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__, template_folder = "../templates", static_folder = "../static")

@app.route("/")
def home():
    return "Hello World"

@app.route("/signin")
def index():
    return render_template("signin.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")