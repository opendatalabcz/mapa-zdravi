from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from .config import ConfigDB


db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)

    # https://stackoverflow.com/questions/15122312/how-to-import-from-config-file-in-flask
    app.config.from_object(ConfigDB)

    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')
    return app
