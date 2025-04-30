from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from application.app import app, db, login_manager
from application.model import Users

def init_db():
    with app.app_context():
        db.create_all()
    if not Users.query.filter_by(email = "admin@gmail.com").first():
        create_admin = Users(name = "admin", email = "admin@gmail.com", password = generate_password_hash("admin"), gender = "Male", is_admin = True )
        db.session.add(create_admin)
        db.session.commit()
        print("Admin Created Successfully!")
    else:
        print("Admin already exists!")


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
            return render_template("signup.html", error = "Email already used")
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = Users(name = name, email = email, password = hashed_password, gender = gender, is_admin = False)
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
            flash("You logged successfully", "success")
            if user.is_admin:
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash("Password is incorrect", "error")
            return render_template("signin.html")
        
    return render_template("signin.html")



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_home.html")

@app.route("/user/dashboard")
def user_dashboard():
    return render_template("user_home.html")

