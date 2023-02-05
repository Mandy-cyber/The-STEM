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
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'q4t7w!z%C*F-JaNdRgUjXn2r5u8x/A?D'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}" #location of db
    db.init_app(app)

    # TODO add views and auth stuff here
    from .views import views
    from .auth import auth
    
    # allowing pages with no prefix
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Messages, MailingList, Resource, SimilarPeople
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        # to get a particular user by their id
        return User.query.get(int(id))

    return app


###### THIS METHOD SEEMS TO NOW BE DEPRECATED :(
# def create_database(app):
#     """ creates a database if it doesn't already exist
#     Args: 
#         app (Flask): a flask app
#     Returns: 
#         None
#     """
#     if not path.exists('website/' + DB_NAME):
#         db.create_all()
#         print("Database created successfully!")