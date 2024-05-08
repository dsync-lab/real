from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

# Function that initializes the db and creates the tables

def db_init(app):
    db.init_app(app)
    login_manager.init_app(app)

    # Creates the tables if the db doesnt already exist
    with app.app_context():
        db.create_all()
        

def register_extensions(app):
    db.init_app(app)
    




def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()