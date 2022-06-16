from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_msearch import Search

import os

basedir=os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
DB_NAME="database.db"
search = Search()

photos = UploadSet('photos', IMAGES)

def create_app():
    app = Flask(__name__)
    app.config['RBAC_USE_WHITE'] = True
    app.config['SECRET_KEY']='Darshan D M Project 1'
    app.config['SQLALCHEMY_DATABASE_URI']= "postgres://aqtemsqdiuebgt:a92569ef88fb8e5fa3d4776d4053df570152b2487b53d46d9512e96e4a088065@ec2-54-157-16-196.compute-1.amazonaws.com:5432/df2dp861v84ioa"
    app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')


    configure_uploads(app,photos) 
    MAX_CONTENT_LENGTH=None
    db.init_app(app)
    search.init_app(app)
    # patch_request_class(app)
    
    from .views import views
    from .auth import auth
    from .add import add
    from .show import show
    from .cart import cart

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(add,url_prefix='/')
    app.register_blueprint(show,url_prefix='/')
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
