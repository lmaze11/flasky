from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(testing=None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if testing is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    from app.models.bike import Bike

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.bike import bike_bp
    app.register_blueprint(bike_bp)

    from .routes.cyclist import cyclist_bp
    app.register_blueprint(cyclist_bp)

    return app

    # flask db migrate -m " message " does migrate
    # flask db upgrade adds the migration and new table to the db

    # "postgresql+psycopg2://postgres:postgres@localhost:5432/bikes_development"
    # app config above hard codes how we can access the db - has to use postgres, pyscogp2, this port, this username, this database name
    # if certain things are changed, we would then not be able to access it
    # good to have separate db for development and for testing (can see that at the end in "bikes_development")
    # for testing we need the db to be completely clean/empty each time - arrange in testing will put stuff into the db and don't want it there every time/day
    # don't want that string living here in this __init__.py
    # we want it in a .env file instead 
    # do "touch .env" in terminal and it will show up to the left screen here
    # can see it as .env with a little gear since it is a settings file
    # is a hidden config file since it is a dot file