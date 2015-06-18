from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap

import os



#create flask 
yoke = Flask(__name__)
yoke.config['DEBUG'] = True
yoke.config['SECRET_KEY'] = 'default'
yoke.config['CSRF_ENABLED'] = True
yoke.config['CSRF_SESSION_KEY'] = 'csrf_secret'

#bootstrap init
bootstrap = Bootstrap()
bootstrap.init_app(yoke)

#init database with yoke
db = SQLAlchemy()
db.init_app(yoke)
db.app = yoke
yoke.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'data.sqlite') 
yoke.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
yoke.config['SQLALCHEMY_RECORD_QUERIES'] = True


#init login_manager with yoke
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth_login'
login_manager.init_app(yoke)



from .auth import auth as auth_blueprint
yoke.register_blueprint(auth_blueprint, url_prefix='/auth')

from .main import main as main_blurprint
yoke.register_blueprint(auth_blueprint)
db.create_all()


