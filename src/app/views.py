from flask import Blueprint, render_template
from .models import DentistsAgeEstimate, Demographics, Students, NRPZS, Insurances, Doctors

from . import db

views = Blueprint('views', __name__)


@views.route('/')
def home():

    # TODO make up what to write here

    return render_template('home.html')


@views.route('/about')
def about():

    # TODO make up what to write here

    import random
    randomlist = random.sample(range(10, 30), 10)

    print(randomlist)

    return render_template('about.html', data=randomlist)


@views.route('/lekari')
def doctors():

    table = Insurances

    # https://docs.sqlalchemy.org/en/14/orm/query.html
    data = db.session.query(
        table.ico, table.expertise_name)

    # print(data.count())
    return render_template('doctors.html', data=data)


@views.route('/mapa')
def map():
    # TODO map + prediction/history
    # TODO update and visualize them based on the input -> create GET, POST here
    import random
    randomlist = random.sample(range(10, 30), 10)

    return render_template('map.html', dummy=randomlist)


@views.route('/statistiky')
def statistics():
    # TODO load statistics
    # TODO update and visualize them based on the input -> create GET, POST here

    return render_template('statistics.html')
