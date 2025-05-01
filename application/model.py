from application.app import app, db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, nullable = False, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    gender = db.Column(db.String, nullable = False)
    is_admin = db.Column(db.Boolean, default = False, nullable = False)
    is_blocked = db.Column(db.Boolean, default = False, nullable = False)

    projects = db.relationship('Projects', lazy = True, backref = 'creator')
    interest = db.relationship('Interest', lazy = True, backref = 'user')
    discussion = db.relationship('Discussion', lazy = True, backref = 'user')


class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    title = db.Column(db.String(50), nullable = False, unique = True)
    description = db.Column(db.Text, nullable = False)
    skills = db.Column(db.String, nullable = False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    interest = db.relationship('Interest', lazy = True, backref = 'project')
    discussion = db.relationship('Discussion', lazy = True, backref = 'project')

class Interest(db.Model):
    __tablename__ = 'interest'
    id = db.Column(db.Integer, nullable = False, primary_key = True)
    users_id = db.Column(db.ForeignKey('users.id'), nullable = False)
    project_id = db.Column(db.ForeignKey('projects.id'), nullable = False)


class Discussion(db.Model):
    __tablename__ = 'discussion'
    id = db.Column(db.Integer, nullable = False, primary_key = True)
    message = db.Column(db.Text, nullable = False )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable = False)










