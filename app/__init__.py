from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy() # db = database and SQLAlchemy = class - outside of func to be imported (if inside func, not able to be imported)
migrate = Migrate() # Migrate class with an instance of migrate


def create_app():
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # need it but not important to know what it does but has to do with older SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:postgres@localhost:5432/bikes_development"

    db.init_app(app)
    migrate.init_app(app, db) # migration is instructions on how to set up my db - wiring flask app, flask server, postgres db, and the migrate tool that sets up the db

    from app.models.bike import Bike # import this class model to the db through migrate - okay that it is not accessed yet

    from .routes.bike import bike_bp # import needs to be inside the func
    app.register_blueprint(bike_bp) # brings in the bp from the bike.py and connects it to the app

    return app

    # flask db migrate -m " message " does migrate
    # flask db upgrade adds the migration and new table to the db