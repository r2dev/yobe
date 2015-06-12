from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import os
basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth_login'

def create():
	yoke = Flask(__name__)
	yoke.config['SECRET_KEY'] = 'ITS HARD'
	yoke.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
	yoke.config['SQLALCHEMY_RECORD_QUERIES'] = True
	yoke.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
	db.init_app(yoke)
	login_manager.init_app(yoke)
	from .auth import auth as auth_blueprint
	yoke.register_blueprint(auth_blueprint, url_prefix='/auth')
	return yoke