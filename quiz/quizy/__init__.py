from email import message
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY='63a7c3e2ac3c7b7ff4fba72b18040fa',
    DATABASE=os.path.join(app.root_path, 'baza.db'),
    SQLALCHEMY_DATABASE_URI='sqlite:///' +
                            os.path.join(app.root_path, 'baza.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    TYTUL='Quizy'
))



db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Proszę się zalogować"
login_manager.login_message_category = 'info'


from quizy import routes