from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from application.app import app, db, login_manager
from application.model import Users, Projects, Interest, Discussion


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
            if user.is_blocked:
                return render_template("signin.html", error = "User blocked by Admin!")
            login_user(user)
            flash("You logged successfully", "success")
            if user.is_admin:
                return redirect(url_for("admin_home"))
            else:
                return redirect(url_for('user_home'))
        else:
            flash("Password is incorrect", "error")
            return render_template("signin.html")
        
    return render_template("signin.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

#<----------------------Admin endpoints---------------------------->
@app.route("/admin/home")
@login_required
def admin_home():
    if not current_user.is_admin:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("user_home"))
    return render_template("admin_home.html")


@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("user_home"))
    users = Users.query.all()
    return render_template("admin_dashboard.html", users = users)


@app.route("/admin/about")
@login_required
def admin_about():
    if not current_user.is_admin:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("user_home"))
    return render_template("admin_about.html")

@app.route("/admin/block_user/<int:user_id>", methods=["POST"])
@login_required
def block_user(user_id):
    if not current_user.is_admin:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("signin"))

    user = Users.query.get_or_404(user_id)
    user.is_blocked = True
    db.session.commit()
    flash(f"User {user.name} has been blocked.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/unblock_user/<int:user_id>", methods=["POST"])
@login_required
def unblock_user(user_id):
    if not current_user.is_admin:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("user_home"))

    user = Users.query.get_or_404(user_id)
    user.is_blocked = False
    db.session.commit()
    flash(f"User {user.name} has been unblocked.", "success")
    return redirect(url_for("admin_dashboard")) 



#<---------------------------------User endpoints-------------------------->
@app.route("/user/home")
@login_required
def user_home():
    user = current_user
    return render_template("user_home.html", user = user)

@app.route("/user/dashboard")
@login_required
def user_dashboard():
    user = current_user
    project = Projects.query.all()
    return render_template("user_dashboard.html", projects = project, user = user)


skills = ['Python', 'Java', 'JavaScript', 'C++', 'C#', 'HTML', 'CSS', 'SQL', 'React', 'Vue.js', 'Angular',
    'Node.js', 'Flask', 'Django', 'Machine Learning', 'Deep Learning', 'Artificial Intelligence', 
    'Blockchain', 'Cloud Computing', 'Docker', 'Kubernetes', 'DevOps', 'Git', 'GitHub', 'Linux', 
    'MongoDB', 'MySQL', 'PostgreSQL', 'TensorFlow', 'PyTorch', 'Data Science', 'Statistics', 'Excel',
    'AWS', 'Azure', 'Google Cloud', 'Swift', 'Kotlin', 'Rust', 'Ruby', 'PHP', 'Firebase', 'Sass', 
    'Tailwind CSS', 'Bootstrap', 'TypeScript', 'GraphQL', 'Web Development', 'Mobile App Development',
    'Game Development', 'VR/AR', 'UI/UX Design', 'UI Design', 'UX Research', 'Software Testing', 
    'Automation Testing', 'Cybersecurity', 'Ethical Hacking', 'SEO', 'Digital Marketing']

@app.route("/user/show", methods = ["GET"])
@login_required
def user_show():
    user = current_user
    project = Projects.query.filter_by(users_id = user.id).all()
    return render_template("user_show.html", projects = project, user = user)
    

@app.route("/user/add", methods = ["GET", "POST"])
@login_required
def user_add():
    user = current_user
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        selected_skills = request.form.getlist('skills')
        skills_str = ",".join(selected_skills)
        if Projects.query.filter_by(title=title).first():
            flash("Project title already exists. Please choose a different", "danger")
            return render_template("user_add.html", skills=skills, user=user)
        if not title or not description or not skills:
            flash("All fields are required", "danger")
            return render_template("user_add.html", skills = skills, user = user)
        new_project = Projects(title = title, description = description, skills = skills_str, users_id = user.id )
        db.session.add(new_project)
        db.session.commit()
        flash("Your Project added successfully", 'success')
        return redirect(url_for('user_add'))
    return render_template("user_add.html", skills = skills, user = user)

@app.route("/user/delete", methods = ["POST"])
@login_required
def user_delete():
    project_id = request.form.get("project_id")
    if not project_id:
        flash("No project specified.", "danger")
        return redirect(url_for("user_show"))
    project = Projects.query.filter_by(id=project_id, users_id=current_user.id).first()
    if not project:
        flash("No project found to delete.", "warning")
        return redirect(url_for('user_show'))
    db.session.delete(project)
    db.session.commit()
    flash("Project Deleted successfully", 'success')
    return redirect(url_for('user_show'))
    

@app.route("/user/update/<int:project_id>", methods = ["GET", "POST"])
@login_required
def user_update(project_id):
    user = current_user
    project = Projects.query.filter(Projects.id == project_id, Projects.users_id == user.id).first()
    if request.method == "POST":
        project.title = request.form['title']
        project.description = request.form['description']
        project.skills = ",".join(request.form.getlist('skills'))
        db.session.commit()
        flash("Poject Updated Successfully", "success")
        return redirect(url_for('user_show'))
    return render_template('user_update.html', project = project, skills = skills, user = user)



@app.route("/user/about")
@login_required
def user_about():
    user = current_user
    return render_template("user_about.html", user = user)

@app.route("/interested", methods = [ "POST"])
@login_required
def interested():
    user = current_user
    project_id = request.form.get("project_id")
    if not project_id:
        flash("No project selected", "danger")
        return redirect(url_for('user_dashboard'))

    existing = Interest.query.filter_by(users_id=user.id, project_id=project_id).first()
    if existing:
        flash("You have already shown interest in this project.", "danger")
        return redirect(url_for('user_dashboard'))
    add_interest = Interest(users_id = user.id, project_id = project_id)
    db.session.add(add_interest)
    db.session.commit()
    flash("Interest added successfully", "success")
    return redirect(url_for('user_dashboard'))

@app.route("/interested/show", methods = ["GET"])
@login_required
def interested_show():
    user = current_user
    interests = Interest.query.all()
    print(len(interests)) 
    interested = Interest.query.filter_by(users_id=user.id).all()
    return render_template("interest.html", interested = interested)


@app.route("/discussion/<int:project_id>", methods=["GET", "POST"])
@login_required
def discussion(project_id):
    user = current_user
    project = Projects.query.get_or_404(project_id)

    if request.method == "POST":
        message = request.form.get("message")
        if not message:
            flash("Message cannot be empty.", "danger")
        else:
            new_message = Discussion(message=message, user_id=user.id, project_id=project.id)
            db.session.add(new_message)
            db.session.commit()
            flash("Comment added!", "success")
            return redirect(url_for('discussion', project_id=project.id))

    comments = Discussion.query.filter_by(project_id=project.id).all()
    return render_template("discussion.html", project=project, comments=comments)


    


    








    


    
    





