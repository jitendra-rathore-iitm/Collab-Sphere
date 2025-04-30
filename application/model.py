from application.app import app, db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    gender = db.Column(db.String, nullable = False)
    is_admin = db.Column(db.Boolean, default = False, nullable = False)


