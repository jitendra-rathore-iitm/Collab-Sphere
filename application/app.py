from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__, template_folder = "../templates", static_folder = "../static")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signin")
def index():
    return render_template("signin.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/admin/home")
def admin_home():
    return render_template("admin_home.html")

@app.route("/user/home")
def user_home():
    return render_template("user_home.html")

@app.route("/admin/about")
def about():
    return render_template("admin_about.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/user/dashboard")
def user_dashboard():
    return render_template("user_home.html")

@app.route("/user/about")
def user_about():
    return render_template("user_about.html")


