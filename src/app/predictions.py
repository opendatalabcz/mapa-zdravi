from urllib import request
from flask import Blueprint, render_template, request
from sqlalchemy import func, distinct, and_, or_, not_

from . import db
from .models import InsurancesPrediction, DoctorsPrediction, NewDoctorsEstimate, DoctorsDistribution
from .queries import get_districts_normalized, get_medical_specialty, get_ws_probability, get_districts_cnt, get_new_doctors


import pandas as pd
from collections import Counter
import math
import numpy as np


WORKDAYS_DICT = {2020: 251,
                 2021: 252,
                 2022: 252,
                 2023: 250,
                 2024: 252,
                 2025: 251,
                 2026: 250,
                 }


def validate_ms(ms):
    doctor_cnt = db.session.query(
        DoctorsPrediction.working_specialty
    ).distinct()
    ds = set(pd.DataFrame(doctor_cnt)[0].unique())

    insurances = db.session.query(
        InsurancesPrediction.medical_specialty
    ).distinct()
    ins = set(pd.DataFrame(insurances)[0].unique())

    common = ds & ins

    ms = set(pd.DataFrame(get_medical_specialty())[0].unique())
    ms_int = list(common & ms)
    ms_int.sort()
    return ms_int


def predict_district(ws, ws_count, year):
    dist_counts = get_districts_cnt(ws, ws_count, year)

    ws_in_dist = pd.DataFrame().from_dict(
        dict(dist_counts), orient='index').reset_index()

    ws_in_dist.columns = ['district', 'new_doctors']
    ws_in_dist['working_specialty'] = ws

    return ws_in_dist


def predict_clk_doctors(pred_year, new_doctors_estimate, ms='all'):
    new_doctors_df = pd.DataFrame()
    for year in range(2022, pred_year+1):
        # predict medical specialty of graduated students
        n_doctors = new_doctors_estimate[(new_doctors_estimate.date_end == year) & (
            new_doctors_estimate.type == 'MUDr.')].doctors_estimate.values[0]

        ws_probability = get_ws_probability()

        np.random.seed(year*n_doctors % 10_000)
        ws_generated = np.random.choice(list(ws_probability.keys()), p=list(
            ws_probability.values()), size=n_doctors)
        ws_counts = Counter(ws_generated)

        # predicts all specialties
        if ms == 'all':
            for ws, ws_count in ws_counts.items():
                ws_in_dist = predict_district(ws, ws_count, year)
                new_doctors_df = pd.concat([new_doctors_df, ws_in_dist])
        # predicts the chosen specialty
        else:
            ws_in_dist = predict_district(ms, ws_counts[ms], year)
            new_doctors_df = pd.concat([new_doctors_df, ws_in_dist])

    if ms != 'all':
        new_doctors_df = new_doctors_df.groupby(
            ['district', 'working_specialty']).sum().reset_index()

    return new_doctors_df


def predict_csk_doctors(pred_year, new_doctors_estimate):
    new_doctors_df = pd.DataFrame()
    for year in range(2022, pred_year+1):
        # predict medical specialty of graduated students
        n_doctors = new_doctors_estimate[(new_doctors_estimate.date_end == year) & (
            new_doctors_estimate.type == 'MDDr.')].doctors_estimate.values[0]

        ws_in_dist = predict_district('stomatologie', n_doctors, year)
        new_doctors_df = pd.concat([new_doctors_df, ws_in_dist])

    new_doctors_df = new_doctors_df.groupby(
        ['district', 'working_specialty']).sum().reset_index()
    return new_doctors_df


def pred_new_doctors(clk_ratio, pred_year, medical_specialty):

    new_doctors_estimate = get_new_doctors(clk_ratio)

    if medical_specialty == 'stomatologie':
        new_doctors = predict_csk_doctors(pred_year, new_doctors_estimate)

    elif medical_specialty == 'všechny specializace' or '--' in medical_specialty:
        new_clk = predict_clk_doctors(pred_year, new_doctors_estimate)
        new_csk = predict_csk_doctors(pred_year, new_doctors_estimate)
        new_doctors = pd.concat([new_clk, new_csk])
        new_doctors = new_doctors.groupby(['district']).sum().reset_index()
        new_doctors['working_specialty'] = 'všechny specializace'

    else:
        new_doctors = predict_clk_doctors(
            pred_year, new_doctors_estimate, medical_specialty)

    new_doctors['capacity'] = 8*60*WORKDAYS_DICT[pred_year] * \
        new_doctors['new_doctors']  # minutes_per_year
    new_doctors = new_doctors[['district', 'capacity']]

    return new_doctors


def pred_map(params):
    clk_ratio = params['clk_ratio']/100
    pred_year = params['pred_year']
    senior_age = params['senior_age']
    hours_weekly = params['hours_weekly']
    ms_value = params['ms_value']

    map_kwargs = {
        'legend_title': 'Čas výkonů / čas lékařů (v %)',
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
        ).group_by(DoctorsPrediction.district).filter(and_(DoctorsPrediction.year == pred_year,
                                                           DoctorsPrediction.senior_age == senior_age))

    doctors_df = pd.DataFrame(
        doctors, columns=['district', 'capacity'])
    insurances_df = pd.DataFrame(
        insurances, columns=['district', 'count', 'time'])

    if pred_year > 2021:
        print('PREDICTION ACTIVE!')
        new_doctors = pred_new_doctors(clk_ratio, pred_year, ms_value)
        print(doctors_df)
        doctors_df = pd.concat([doctors_df, new_doctors])
        doctors_df = doctors_df.groupby('district').sum().reset_index()
        print(doctors_df)

    capacity = pd.merge(doctors_df, insurances_df, on='district')
    # in case doctors work work longer than fulltime
    capacity['capacity'] = round(capacity['capacity'] * hours_weekly / 40)
    # compute capacity
    capacity['workload'] = round(100*capacity['time'] / capacity['capacity'])

    # Medical specialty query
    med_spec = get_medical_specialty()
    med_spec_val = validate_ms(med_spec)
    map_kwargs['medical_specialties'] = ['všechny specializace'] + med_spec_val
    # Demographics query
    demo_df, normalized = get_districts_normalized()
    map_kwargs['normalized_names'] = normalized

    df = pd.merge(capacity, demo_df, on='district')

    df = df.sort_values('workload', ascending=False).reset_index(drop=True)
    map_kwargs['data'] = pd.Series(
        df.workload.values, index=df.normalized).to_dict()

    # legend labels
    map_kwargs['legend_labels'] = [
        75, 100, 125, 150, 200, 500, 'Data nedostupná']

    return map_kwargs
