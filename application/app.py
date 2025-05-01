from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__, template_folder = "../templates", static_folder = "../static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ehdyrfgsjfhbjgiddhow'


db = SQLAlchemy(app)
migarate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from application import model, routes




