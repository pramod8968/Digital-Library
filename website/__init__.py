from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_uploads import IMAGES, UploadSet, configure_uploads

import os

basedir=os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
DB_NAME="database.db"

photos = UploadSet('photos', IMAGES)

def create_app():
    app = Flask(__name__)
    app.config['RBAC_USE_WHITE'] = True
    app.config['SECRET_KEY']='Darshan D M Project 1'
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}'
    app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')


    configure_uploads(app,photos) 
    MAX_CONTENT_LENGTH=None
    db.init_app(app)
    # patch_request_class(app)
    
    from .views import views
    from .auth import auth
    from .add import add
    from .departments import dep
    from .semesters import sem 
    from .cart import cart

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(add,url_prefix='/')
    app.register_blueprint(dep,url_prefix='/')
    app.register_blueprint(sem,url_prefix='/')
    app.register_blueprint(cart,url_prefix='/')
    from .models import User

    create_database(app)

    #modified code
    #user_manager = UserManager(app, db, User)
    #user_manager.init_app(db_adapter,app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
