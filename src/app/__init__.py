from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '46s85h4r5j4htdjhs4h56tjd4jnn8sdtj4d8m4d'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'TODO'

    # db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
