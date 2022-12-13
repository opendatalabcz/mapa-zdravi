from urllib import request
from flask import Blueprint, render_template, request
from .models import DentistsAgeEstimate, Demographics, Students, NRPZS, Insurances, Doctors, MedicalSpecialty, InsurancesPrediction, DoctorsPrediction
from sqlalchemy import func, distinct, and_, or_, not_


from . import db

import pandas as pd
import random
import re
import unidecode

views = Blueprint('views', __name__)


def pred_map(params):

    clk_ratio = params['clk_ratio']
    pred_year = params['pred_year']
    senior_age = params['senior_age']
    hours_weekly = params['hours_weekly']

    ms_value = request.form.get('medical_specialty')

    map_kwargs = {
        'legend_title': 'Vykázané výkony / úvazky lékařů (v %)',
        'ratio_label': ' %',
        'legend_ascending': False
    }

    if request.method == 'POST' and ms_value != 'všechny specializace' and not '--' in ms_value:
        print(ms_value)
        insurances = db.session.query(
            InsurancesPrediction.district,
            InsurancesPrediction.count_population,
            InsurancesPrediction.time_population,
        ).filter(and_(InsurancesPrediction.year == pred_year,
                      InsurancesPrediction.medical_specialty == ms_value))

        doctors = db.session.query(
            DoctorsPrediction.district,
            DoctorsPrediction.minutes_per_year,
            DoctorsPrediction.mpwpd_per_speciality,
        ).filter(and_(DoctorsPrediction.year == pred_year,
                      DoctorsPrediction.senior_age == senior_age,
                      DoctorsPrediction.working_specialty == ms_value))

    else:
        ms_value = 'všechny specializace'

        insurances = db.session.query(
            InsurancesPrediction.district,
            func.sum(InsurancesPrediction.count_population).label('cnt_total'),
            func.sum(InsurancesPrediction.time_population).label('time_total'),
        ).group_by(InsurancesPrediction.district).filter(and_(InsurancesPrediction.year == pred_year))

        doctors = db.session.query(
            DoctorsPrediction.district,
            func.sum(DoctorsPrediction.minutes_per_year).label('capacity'),
            func.sum(DoctorsPrediction.mpwpd_per_speciality,
                     ).label('capacity_daily'),
        ).group_by(DoctorsPrediction.district).filter(and_(DoctorsPrediction.year == pred_year,
                                                           DoctorsPrediction.senior_age == senior_age))

    map_kwargs['map_title'] = 'Časové zatížení - ' + ms_value
    map_kwargs['ms_value'] = ms_value

    doctors_df = pd.DataFrame(
        doctors, columns=['district', 'capacity', 'capacity_daily'])
    insurances_df = pd.DataFrame(
        insurances, columns=['district', 'count', 'time'])

    capacity = pd.merge(doctors_df, insurances_df, on='district')
    # in case doctors work work longer than fulltime
    capacity['capacity'] = round(capacity['capacity'] * hours_weekly / 40)
    # compute capacity
    capacity['workload'] = round(100*capacity['time'] / capacity['capacity'])

    # Medical specialty query
    map_kwargs['medical_specialties'] = db.session.query(
        MedicalSpecialty.medical_specialty_name,
        MedicalSpecialty.id
    ).distinct().order_by(MedicalSpecialty.id)

    map_kwargs['ms_value'] = ms_value

    # Demographics query
    demo_cnt = db.session.query(
        Demographics.district,
        Demographics.population,
        Demographics.normalized
    ).filter(Demographics.year == 2021)

    demo_df = pd.DataFrame(
        demo_cnt, columns=['district', 'population', 'normalized'])
    map_kwargs['normalized_names'] = pd.Series(
        demo_df.district.values, index=demo_df.normalized).to_dict()

    df = pd.merge(capacity, demo_df, on='district')

    df = df.sort_values('workload', ascending=False).reset_index(drop=True)
    map_kwargs['data'] = pd.Series(
        df.workload.values, index=df.normalized).to_dict()

    # legend labels
    map_kwargs['legend_labels'] = [
        75, 100, 125, 150, 200, 500, 'Data nedostupná']

    return map_kwargs


@views.route('/mapa', methods=['GET', 'POST'])
def map():

    if request.method == 'POST':
        param_kwargs = {
            'clk_ratio': int(request.form.get('clk_ratio')),
            'pred_year': int(request.form.get('pred_year')),
            'senior_age': int(request.form.get('senior_age')),
            'hours_weekly': int(request.form.get('hours_weekly')),
        }
    else:
        param_kwargs = {
            'clk_ratio': 72,
            'pred_year': 2021,
            'senior_age': 65,
            'hours_weekly': 40,
        }
    print(param_kwargs)

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
        'legend_ascending': True
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
    map_kwargs['medical_specialties'] = db.session.query(
        MedicalSpecialty.medical_specialty_name,
    ).distinct().order_by(MedicalSpecialty.id)

    map_kwargs['ms_value'] = ms_value

    # Demographics query
    demo_cnt = db.session.query(
        Demographics.district,
        Demographics.population,
        Demographics.normalized
    ).filter(Demographics.year == 2021)

    demo_df = pd.DataFrame(
        demo_cnt, columns=['district', 'population', 'normalized'])
    map_kwargs['normalized_names'] = pd.Series(
        demo_df.district.values, index=demo_df.normalized).to_dict()

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

    # doctors age query
    doctor_cnt = db.session.query(
        Doctors.graduated_year,
        func.count(distinct(Doctors.doctor_id))
    ).group_by(Doctors.graduated_year)\
        .filter(and_(Doctors.graduated_year < 2022.,
                     Doctors.graduated_year > 2011.))

    new_doctors_kwargs['new_doctors'] = list(dict(doctor_cnt).values())
    new_doctors_kwargs['years'] = list(dict(doctor_cnt).keys())

    graduates_cnt = db.session.query(
        Students.date_end,
        func.count(distinct(Students.id))
    ).group_by(Students.date_end)\
        .filter(and_(Students.date_end < 2022.,
                     Students.date_end > 2011.,
                     Students.major == 'Všeobecné lékařství',
                     Students.graduated == True,))

    new_doctors_kwargs['graduates'] = list(dict(graduates_cnt).values())

    return new_doctors_kwargs


def students():
    students_kwargs = {
    }

    students = db.session.query(
        Students.id,
        Students.graduated,
        Students.citizenship,
        Students.date_end,
    ).filter(and_(Students.date_end > 2011.,
                  Students.citizenship.isnot(None),
                  Students.citizenship != 'NaN',
                  Students.date_end.isnot(None)))

    students = pd.DataFrame(
        students, columns=['_id', 'graduated', 'citizenship', 'date_end'])
    students = students[~students.citizenship.isna()].drop_duplicates('_id')
    # students.date_end = students.date_end.astype(int)
    students.loc[~students.citizenship.isin(
        ['CZE', 'SVK']), 'citizenship'] = 'Ostatní'

    graduated = students[(students.graduated == True) & (
        students.date_end < 2022) & (~students.citizenship.isna())
    ].rename(columns={'graduated': 'count'})

    graduated = graduated.groupby(['citizenship', 'date_end'])[
        'count'].count().reset_index()

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
