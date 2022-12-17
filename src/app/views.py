from urllib import request
from flask import Blueprint, render_template, request
from sqlalchemy import func, distinct, and_, or_, not_

from . import db
from .models import Doctors

from .queries import get_districts_normalized, get_medical_specialty, get_clk_graduates, get_docs_cnt_range, get_student_citizenship

import pandas as pd


views = Blueprint('views', __name__)


@views.route('/mapa', methods=['GET', 'POST'])
def map():
    if request.method == 'POST':
        param_kwargs = {
            'clk_ratio': int(request.form.get('clk_ratio')),
            'pred_year': int(request.form.get('pred_year')),
            'senior_age': int(request.form.get('senior_age')),
            'hours_weekly': int(request.form.get('hours_weekly')),
            'ms_value': request.form.get('medical_specialty'),
            'map_title': f'Výkonnostní kapacita - {request.form.get("medical_specialty")}',
        }
    else:
        param_kwargs = {
            'clk_ratio': 72,
            'pred_year': 2021,
            'senior_age': 65,
            'hours_weekly': 40,
            'ms_value': 'všechny specializace',
            'map_title': f'Výkonnostní kapacita - všechny specializace',
        }
    print(param_kwargs)

    from .predictions import pred_map

    map_kwargs = pred_map(param_kwargs)

    return render_template('map.html',
                           **map_kwargs,
                           **param_kwargs,
                           )

# -------------------------------------------------------------


@views.route('/news')
def news():
    return render_template('news.html')

# -------------------------------------------------------------


@views.route('/about')
def about():
    return render_template('about.html')

# -------------------------------------------------------------


@views.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# -------------------------------------------------------------


@ views.route('/', methods=['GET', 'POST'])
def home():
    map_kwargs = {
        'legend_title': 'Počet lékařů / 10 tis. obyv.',
        'ratio_label': ' / 10 000 obyvatel',
        'map_coloring': 'capacity_map'
    }

    ms_value = request.form.get('medical_specialty')
    if request.method == 'POST' and ms_value != 'všechny specializace' and not '--' in ms_value:
        # print(ms_value)
        doctor_cnt = db.session.query(
            Doctors.district,
            func.count(distinct(Doctors.doctor_id))
        ).group_by(Doctors.district).filter(Doctors.medical_specialty == ms_value)
    else:
        ms_value = 'všechny specializace'
        doctor_cnt = db.session.query(
            Doctors.district,
            func.count(distinct(Doctors.doctor_id))
        ).group_by(Doctors.district)

    map_kwargs['ms_value'] = ms_value
    map_kwargs['map_title'] = 'Počet lékařů - ' + ms_value

    doctor_df = pd.DataFrame(doctor_cnt, columns=['district', 'n_doctors'])

    # Medical specialty query
    map_kwargs['medical_specialties'] = get_medical_specialty()

    demo_df, normalized = get_districts_normalized()
    map_kwargs['normalized_names'] = normalized

    df = pd.merge(doctor_df, demo_df, on='district')
    df['ratio'] = round(10000 * df.n_doctors / df.population, 2)
    df = df.sort_values('ratio', ascending=False).reset_index(drop=True)
    map_kwargs['data'] = pd.Series(
        df.ratio.values, index=df.normalized).to_dict()

    # legend labels
    vals = list(df['ratio'].quantile(
        [.2, .3, .5, .65, .75, .90, .95]).values)
    map_kwargs['legend_labels'] = [round(n, 2)
                                   for n in vals] + ['Data nedostupná']

    return render_template('home.html',
                           **map_kwargs,
                           top5=df.head(),
                           worst5=df.tail().iloc[::-1]
                           )

# -------------------------------------------------------------


def age_map():
    map_kwargs = {
        'map_title': 'Průměrný věk lékařů',
        'legend_title': 'Průměrný věk',
        'ratio_label': ' let',
        'map_coloring': 'age_map'
    }

    # demographics query
    demo_df, normalized = get_districts_normalized()
    map_kwargs['normalized_names'] = normalized

    # doctors age query
    doctor_cnt = db.session.query(
        Doctors.district,
        Doctors.age_estimate
    ).distinct(Doctors.district, Doctors.doctor_id)

    doctor_df = pd.DataFrame(doctor_cnt, columns=[
                             'district', 'age_estimate'])
    doctor_df = pd.merge(doctor_df, demo_df, on='district')[
        ['normalized', 'age_estimate']]
    district_ages = doctor_df.groupby(
        'normalized').mean().apply(lambda x: round(x, 2)).sort_values('age_estimate')
    ages = pd.Series(district_ages.age_estimate.values,
                     index=district_ages.index).to_dict()

    map_kwargs['data'] = ages
    # legend labels

    map_kwargs['legend_labels'] = [
        50, 52, 55, 58, 60, 'Data nedostupná']

    return map_kwargs


def new_doctors():
    new_doctors_kwargs = {
    }

    new_docs_cnt = get_docs_cnt_range(year_from=2012, year_to=2021)

    new_doctors_kwargs['new_doctors'] = new_docs_cnt
    new_doctors_kwargs['years'] = list(range(2012, 2022))

    new_doctors_kwargs['graduates'] = get_clk_graduates()

    return new_doctors_kwargs


def students():
    students_kwargs = {
    }

    graduated = get_student_citizenship()

    students_kwargs['graduated_czechs'] = graduated[graduated.citizenship ==
                                                    'CZE']['count'].to_list()

    students_kwargs['graduated_slovaks'] = graduated[graduated.citizenship ==
                                                     'SVK']['count'].to_list()

    students_kwargs['graduated_others'] = graduated[graduated.citizenship ==
                                                    'Ostatní']['count'].to_list()

    return students_kwargs


@ views.route('/statistiky')
def statistics():

    map_kwargs = age_map()

    new_doctors_kwargs = new_doctors()

    student_kwargs = students()

    # TODO create and upload statistics
    return render_template('statistics.html',
                           **map_kwargs,
                           **new_doctors_kwargs,
                           **student_kwargs)
