from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from flask_migrate import Migrate

from os import path
from .config import ConfigDB, ConfigDBdev


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app(prod=True):
    app = Flask(__name__)

    # https://stackoverflow.com/questions/15122312/how-to-import-from-config-file-in-flask
    print(f"PROD FLAG {prod}")
    if prod:
        app.config.from_object(ConfigDB)
    else:
        app.config.from_object(ConfigDBdev)

    # app.config.from_object(ConfigDB)
    db.init_app(app)

    # migrate = Migrate(app, db)

    from .views import views

    app.register_blueprint(views, url_prefix="/")
    return app
