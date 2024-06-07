from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask import current_app

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) # initialise the database with Flask application
    
    from .views import views
    from .auth import auth
    # dot before file name represent relative import which is used to import file in a Python package that is also in this Python package
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    from .models import User, Post, Comment, Like # before creating database we want our models to be imported individually
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login" # where to redirect users who are not logged in and try to access the page
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) 
    
    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME): # check if path from () exists
        with app.app_context():
            db.create_all()
        print("Created database!")