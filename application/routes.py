from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from application.app import app, db, login_manager
from application.model import Users

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']

        if Users.query.filter_by(email = email).first():
            return render_template("signup.html", error = "Email already taken by anyone!")
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = Users(name = name, email = email, password = hashed_password, gender = gender)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("signin"))


    return render_template("signup.html")

    

@app.route("/signin", methods = ["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email = email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return render_template("admin_dashboard.html")
        else:
            return render_template("signin.html", error = "Inavalid user or password")
        
    return render_template("signin.html")





@app.route("/logout")
def logout():
    user = user.query.filter_by(email = current_user).first()
    logout_user()
    return redirect(url_for("signin"))

