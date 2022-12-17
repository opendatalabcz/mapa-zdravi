from urllib import request
from flask import Blueprint, render_template, request
from sqlalchemy import func, distinct, and_, or_, not_

from . import db
from .models import DentistsAgeEstimate, Demographics, Students, NRPZS, Insurances, Doctors, MedicalSpecialty, InsurancesPrediction, DoctorsPrediction, DoctorsDistribution, NewDoctorsEstimate, NewDoctorsPrecomputed

import pandas as pd
import numpy as np
from collections import Counter
import math


def get_districts_normalized():
    # Demographics query
    demo_cnt = db.session.query(
        Demographics.district,
        Demographics.population,
        Demographics.normalized
    ).distinct(Demographics.district).filter(Demographics.year == 2021)

    demo_df = pd.DataFrame(
        demo_cnt, columns=['district', 'population', 'normalized'])
    normalized = pd.Series(
        demo_df.district.values, index=demo_df.normalized).to_dict()

    return demo_df, normalized


def get_medical_specialty():
    ms = db.session.query(
        MedicalSpecialty.medical_specialty_name,
    ).distinct().order_by(MedicalSpecialty.id)
    return ms


def get_ws_probability():
    doctors_distribution = db.session.query(
        DoctorsDistribution.working_specialty,
    ).filter(DoctorsDistribution.graduated_year >= 2015)

    doctors_distribution = pd.DataFrame(doctors_distribution, columns=[
                                        'working_specialty'])
    working_specialty = doctors_distribution[(
        doctors_distribution['working_specialty'] != 'stomatologie')]['working_specialty'].value_counts(normalize=True)
    ws_probability = dict(
        zip(working_specialty.index, working_specialty.values))
    return ws_probability


def get_districts_cnt(ws, ws_count, year):
    if ws == 'stomatologie':
        filt = DoctorsDistribution.working_specialty == ws
    else:
        filt = and_(DoctorsDistribution.graduated_year >= 2015,
                    DoctorsDistribution.working_specialty == ws)

    doctors_distribution = db.session.query(
        DoctorsDistribution.district,
    ).distinct(DoctorsDistribution.doctor_id,
               DoctorsDistribution.working_specialty)\
        .filter(filt)

    doctors_distribution = pd.DataFrame(doctors_distribution, columns=[
                                        'district'])

    district_probability = doctors_distribution['district'].value_counts(True)

    np.random.seed(ws_count*year % 10_000)
    if not district_probability.empty:
        ws_district_generated = np.random.choice(list(
            district_probability.index), p=list(district_probability.values), size=ws_count)
    else:
        ws_district_generated = np.random.choice(
            doctors_distribution.district.unique(), size=ws_count)

    dist_counts = Counter(ws_district_generated)
    return dist_counts


def get_new_doctors(clk_ratio):

    nd_estimate = db.session.query(
        NewDoctorsEstimate.date_end,
        NewDoctorsEstimate.graduate_estimate,
        NewDoctorsEstimate.type,
    )

    new_doctors_estimate = pd.DataFrame(nd_estimate, columns=[
                                        'date_end', 'graduate_estimate', 'type'])

    new_doctors_estimate['doctors_estimate'] = (
        new_doctors_estimate['graduate_estimate'] * clk_ratio).apply(math.ceil)

    return new_doctors_estimate


def get_new_doctors_db(clk_ratio, pred_year, ms):

    if ms == 'všechny specializace':
        filt = and_(NewDoctorsPrecomputed.year <= pred_year,
                    NewDoctorsPrecomputed.clk_ratio == clk_ratio)
    else:
        filt = and_(NewDoctorsPrecomputed.working_specialty == ms,
                    NewDoctorsPrecomputed.year <= pred_year,
                    NewDoctorsPrecomputed.clk_ratio == clk_ratio)
    new_docs_query = db.session.query(
        NewDoctorsPrecomputed.district,
        func.sum(distinct(NewDoctorsPrecomputed.new_doctors))
    ).group_by(NewDoctorsPrecomputed.district)\
        .filter(filt)

    new_doctors = pd.DataFrame(new_docs_query, columns=[
                               'district', 'new_doctors'])
    return new_doctors


def get_clk_graduates():
    graduates_cnt = db.session.query(
        Students.date_end,
        func.count(distinct(Students.id))
    ).group_by(Students.date_end)\
        .filter(and_(Students.date_end < 2022.,
                     Students.date_end > 2011.,
                     Students.major == 'Všeobecné lékařství',
                     Students.graduated == True,))

    grad_res = list(dict(graduates_cnt).values())
    return grad_res


def get_docs_cnt_range(year_from, year_to):
    # doctors age query
    doctor_cnt = db.session.query(
        Doctors.graduated_year,
        func.count(distinct(Doctors.doctor_id))
    ).group_by(Doctors.graduated_year)\
        .filter(and_(Doctors.graduated_year < 2022.,
                     Doctors.graduated_year > 2011.))

    doctor_cnt_list = list(dict(doctor_cnt).values())
    return doctor_cnt_list


def get_student_citizenship():
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

    print(graduated)
    return graduated
