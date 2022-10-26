from flask import Blueprint, render_template
from .models import DentistsAgeEstimate, Demographics, Students, NRPZS, Insurances, Doctors
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


@views.route('/lekari')
def doctors():

    # https://docs.sqlalchemy.org/en/14/orm/query.html
    doctor_cnt = db.session.query(
        Doctors.district,
        func.count(Doctors.doctor_id)
    ).group_by(Doctors.district)

    doctor_df = pd.DataFrame(doctor_cnt, columns=['district', 'n_doctors'])
    demo_cnt = db.session.query(
        Demographics.district,
        Demographics.population
    ).filter(Demographics.year == 2021)

    demo_df = pd.DataFrame(demo_cnt, columns=['district', 'population'])
    df = pd.merge(doctor_df, demo_df, on='district')
    df['ratio'] = round(10000 * df.n_doctors / df.population, 2)
    data = df[['district', 'ratio']].values.tolist()
    return render_template('doctors.html', data=data)


@ views.route('/mapa')
def map():
    # TODO map + prediction/history
    # TODO update and visualize them based on the input -> create GET, POST here

    # Medical specialty query
    medical_specialties = db.session.query(
        Doctors.medical_specialty).distinct()

    doctor_cnt = db.session.query(
        Doctors.district,
        func.count(distinct(Doctors.doctor_id))
    ).group_by(Doctors.district)

    doctor_df = pd.DataFrame(doctor_cnt, columns=['district', 'n_doctors'])

    # Demographics query
    demo_cnt = db.session.query(
        Demographics.district,
        Demographics.population
    ).filter(Demographics.year == 2021)

    demo_df = pd.DataFrame(demo_cnt, columns=['district', 'population'])

    df = pd.merge(doctor_df, demo_df, on='district')
    df.loc[df.district == 'Praha', 'district'] = 'Hlavní město Praha'
    df['ratio'] = round(10000 * df.n_doctors / df.population, 2)
    df['normalized'] = df['district'].apply(unidecode.unidecode)
    df['normalized'] = df['normalized'].apply(
        lambda x: re.sub('[^a-z]', '', x.lower()))

    df = df.sort_values('ratio', ascending=False).reset_index(drop=True)
    ratios = pd.Series(df.ratio.values, index=df.normalized).to_dict()
    normalized_names = pd.Series(
        df.district.values, index=df.normalized).to_dict()

    legend_labels = [20, 40, 60, 80, 90, 100, 'Data nedostupná']

    return render_template('map.html',
                           legend_labels=legend_labels,
                           medical_specialties=medical_specialties,
                           ratios=ratios,
                           normalized_names=normalized_names,
                           top5=df.head(),
                           worst5=df.tail().iloc[::-1])


@ views.route('/statistiky')
def statistics():
    # TODO load statistics
    # TODO update and visualize them based on the input -> create GET, POST here

    return render_template('statistics.html')
