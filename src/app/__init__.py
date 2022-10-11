from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '46s85h4r5j4htdjhs4h56tjd4jnn8sdtj4d8m4d'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_NAME}' # TODO setup postresql db
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import DentistsAgeEstimate, Demographics, Students, NRPZS, InsuranceCodes, Insurances, Doctors

    # df = pandas.read_csv(csvfile)
    # df.to_sql(table_name, conn, if_exists='append', index=False)
    create_database(app)

    return app


def create_database(app):
    if not path.exists(f'app/{DB_NAME}'):
        with app.app_context():
            db.create_all()
        print('Database created.')
