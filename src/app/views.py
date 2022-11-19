from urllib import request
from flask import Blueprint, render_template, request
from .models import DentistsAgeEstimate, Demographics, Students, NRPZS, Insurances, Doctors, MedicalSpecialty
from sqlalchemy import func, distinct


from . import db

import pandas as pd
import random
import re
import unidecode

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


@views.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# -------------------------------------------------------------


@ views.route('/mapa', methods=['GET', 'POST'])
def map():
    # TODO prediction/history
    # TODO update and visualize them based on the input -> create GET, POST here

    if request.method == 'POST' and request.form.get('medical_specialty') != 'Všechny obory':
        ms_value = request.form.get('medical_specialty')
        print(ms_value)
        doctor_cnt = db.session.query(
            Doctors.district,
            func.count(distinct(Doctors.doctor_id))
        ).group_by(Doctors.district).filter(Doctors.medical_specialty.contains(ms_value))
    else:
        ms_value = 'celkem'
        doctor_cnt = db.session.query(
            Doctors.district,
            func.count(distinct(Doctors.doctor_id))
        ).group_by(Doctors.district)

    doctor_df = pd.DataFrame(doctor_cnt, columns=['district', 'n_doctors'])

    # Medical specialty query
    ms = db.session.query(
        MedicalSpecialty.medical_specialty_name,
        MedicalSpecialty.id
    ).distinct().order_by(MedicalSpecialty.id)

    # Demographics query
    demo_cnt = db.session.query(
        Demographics.district,
        Demographics.population,
        Demographics.normalized
    ).filter(Demographics.year == 2021)

    demo_df = pd.DataFrame(
        demo_cnt, columns=['district', 'population', 'normalized'])
    normalized_names = pd.Series(
        demo_df.district.values, index=demo_df.normalized).to_dict()

    df = pd.merge(doctor_df, demo_df, on='district')
    df['ratio'] = round(10000 * df.n_doctors / df.population, 2)
    df = df.sort_values('ratio', ascending=False).reset_index(drop=True)
    ratios = pd.Series(df.ratio.values, index=df.normalized).to_dict()

    # legend labels
    vals = list(df['ratio'].quantile(
        [.2, .3, .5, .65, .75, .90, .95]).values)
    legend_labels = [round(n, 2) for n in vals] + ['Data nedostupná']
    print(legend_labels)

    map_kwargs = {
        'map_title': 'Počet lékařů',
        'legend_title': 'Počet lékařů / 10 tis. obyv.',
        'ratio_label': ' / 10 000 obyvatel',
        'legend_ascending': True
    }

    print(map_kwargs)

    return render_template('map.html',
                           legend_labels=legend_labels,
                           medical_specialties=ms,
                           ratios=ratios,
                           normalized_names=normalized_names,
                           top5=df.head(),
                           worst5=df.tail().iloc[::-1],
                           **map_kwargs)

# -------------------------------------------------------------


def age_map():
    map_kwargs = {
        'map_title': 'Průměrný věk lékařů',
        'legend_title': 'Průměrný věk',
        'ratio_label': ' let',
        'legend_ascending': False
    }

    # demographics query
    demo_cnt = db.session.query(
        Demographics.district,
        Demographics.normalized
    ).distinct(Demographics.district)

    demo_df = pd.DataFrame(demo_cnt, columns=['district', 'normalized'])
    normalized_names = pd.Series(
        demo_df.district.values, index=demo_df.normalized).to_dict()

    map_kwargs['normalized_names'] = normalized_names

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
        'normalized').mean().apply(lambda x: round(x, 2))
    ratios = pd.Series(district_ages.age_estimate.values,
                       index=district_ages.index).to_dict()

    map_kwargs['ratios'] = ratios

    # legend labels
    vals = list(district_ages['age_estimate'].quantile(
        [.2, .3, .5, .65, .75, .90, .95]).values)
    map_kwargs['legend_labels'] = [round(n, 2) for n in vals]
    return map_kwargs


@ views.route('/statistiky')
def statistics():

    map_kwargs = age_map()

    # TODO create and upload statistics
    return render_template('statistics.html', **map_kwargs)
