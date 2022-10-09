from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html')


@views.route('/about')
def about():
    return render_template('about.html')


@views.route('/lekari')
def doctors():
    return render_template('doctors.html')


@views.route('/mapa')
def map():
    return render_template('map.html')


@views.route('/statistiky')
def statistics():
    return render_template('statistics.html')

# TODO statistiky a vizualizace
