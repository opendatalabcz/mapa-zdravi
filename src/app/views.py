from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():

    # TODO make up what to write here

    return render_template('home.html')


@views.route('/about')
def about():

    # TODO make up what to write here

    return render_template('about.html')


class TestDocs():
    def __init__(self, doctor_name, doctor_url) -> None:
        self.doctor_url = doctor_url
        self.doctor_name = doctor_name


@views.route('/lekari')
def doctors():

    # TODO load doctors

    # Test
    doctors = []
    for i in range(300):
        doctors.append(TestDocs(f'name{i}', 'xxx'))

    return render_template('doctors.html', doctors=doctors)


@views.route('/mapa')
def map():
    # TODO map + prediction/history
    # TODO update and visualize them based on the input -> create GET, POST here
    return render_template('map.html')


@views.route('/statistiky')
def statistics():
    # TODO load statistics
    # TODO update and visualize them based on the input -> create GET, POST here

    return render_template('statistics.html')
