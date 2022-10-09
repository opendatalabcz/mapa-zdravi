
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# from sqlalchemy import Column, Integer, Unicode, DateTime, Boolean, Float, Date, ForeignKey, Index, ARRAY, Time
# from sqlalchemy.orm import relationship


class Demographics(db.Model):
    __tablename__ = 'Demografické údaje'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100))
    nuts_code = db.Column(db.String(20))
    year = db.Column(db.Integer)

    population = db.Column(db.Integer)
    born = db.Column(db.Integer)
    deceased = db.Column(db.Integer)
    born_deceased = db.Column(db.Integer)
    immigrants = db.Column(db.Integer)
    emigrants = db.Column(db.Integer)
    migration = db.Column(db.Integer)
    change_total = db.Column(db.Integer)
    # population_total = db.Column(db.Integer)

    population_under_15 = db.Column(db.Integer)
    population_15_64 = db.Column(db.Integer)
    population_over_64 = db.Column(db.Integer)
    avg_age_total = db.Column(db.Float)
    avg_index_total = db.Column(db.Float)

    female_under_15 = db.Column(db.Integer)
    female_15_64 = db.Column(db.Integer)
    female_over_64 = db.Column(db.Integer)
    female_avg_age = db.Column(db.Float)
    female_avg_index = db.Column(db.Float)

    male_under_15 = db.Column(db.Integer)
    male_15_64 = db.Column(db.Integer)
    male_over_64 = db.Column(db.Integer)
    male_avg_age = db.Column(db.Float)
    male_avg_index = db.Column(db.Float)

    last_access = db.Column(db.DateTime(timezone=True), default=func.now())
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Students(db.Model):
    __tablename__ = 'Studenti'

    id = db.Column(db.Integer, primary_key=True)

    age_end = db.Column(db.Integer)
    age_now = db.Column(db.Integer)
    age_start = db.Column(db.Integer)

    birth_date = db.Column(db.Integer)
    citizenship = db.Column(db.Unicode(100))

    date_end = db.Column(db.Integer)
    date_now = db.Column(db.Integer)

    degree = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    graduated = db.Column(db.Boolean)

    language = db.Column(db.String(5))
    major = db.Column(db.String(50))

    permanent_address = db.Column(db.String(500))
    relevance_date = db.Column(db.DateTime)
    study_length = db.Column(db.Integer)
    university = db.Column(db.String(10))

    year_of_study = db.Column(db.Integer)
    year_for_degree = db.Column(db.Integer)
    years_extra = db.Column(db.Integer)

    dropout = db.Column(db.Boolean)

    last_access = db.Column(db.DateTime(timezone=True), default=func.now())


class DentistsAgeEstimate(db.Model):
    __tablename__ = 'Odhadované věkové rozložení dentistů'

    id = db.Column(db.Integer, primary_key=True)
    age_end_estimate = db.Column(db.Integer)
    date_end_estimate = db.Column(db.Integer)
    age_now_estimate = db.Column(db.Integer)
    last_access = db.Column(db.DateTime(timezone=True), default=func.now())


#  TODO Insurance companies
#  TODO Insurance companies
