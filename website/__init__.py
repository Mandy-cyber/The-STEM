from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "stemdatabase.db"

def create_app():
    """ create a new Flask 'app' (website)
    Args: 
        None
    Returns:
        app (Flask): the flask app
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '' #encrypt session data
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}" #location of db
    db.init_app(app)

    # TODO add views and auth stuff here

    return app


def create_database(app):
    """ creates a database if it doesn't already exist
    Args: 
        app (Flask): a flask app
    Returns: 
        None
    """
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Database created successfully!")