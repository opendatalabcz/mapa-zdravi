from urllib import request
from flask import Blueprint, render_template, request
from sqlalchemy import func, distinct, and_, or_, not_

from . import db
from .models import DentistsAgeEstimate, Demographics, Students, NRPZS, Insurances, Doctors, MedicalSpecialty, InsurancesPrediction, DoctorsPrediction, DoctorsDistribution, NewDoctorsEstimate

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

    doctors_distribution = db.session.query(
        DoctorsDistribution.district,
    ).distinct(DoctorsDistribution.doctor_id,
               DoctorsDistribution.working_specialty)\
        .filter(and_(DoctorsDistribution.graduated_year >= 2015,
                     DoctorsDistribution.working_specialty == ws))

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
