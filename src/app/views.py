from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html')


@views.route('/about')
def about():
    return render_template('about.html')


class Docs():
    def __init__(self, doctor_name, doctor_url) -> None:
        self.doctor_url = doctor_url
        self.doctor_name = doctor_name


@views.route('/lekari')
def doctors():

    # TODO load doctors
    doctors = []
    for i in range(3):
        doctors.append(Docs(f'name{i}', 'xxx'))

    return render_template('doctors.html', doctors=doctors)


@views.route('/mapa')
def map():
    return render_template('map.html')


@views.route('/statistiky')
def statistics():
    return render_template('statistics.html')
