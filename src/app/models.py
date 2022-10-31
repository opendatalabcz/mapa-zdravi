
from . import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


# TODO add relations

class DentistsAgeEstimate(db.Model):
    __tablename__ = 'DentistsAgeEstimate'

    id = db.Column(db.Integer, primary_key=True)
    age_end_estimate = db.Column(db.Integer)
    date_end_estimate = db.Column(db.Integer)
    age_now_estimate = db.Column(db.Integer)
    last_access = db.Column(db.DateTime(timezone=True), default=func.now())


class Students(db.Model):
    __tablename__ = 'students'

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


class Demographics(db.Model):
    __tablename__ = 'demographics'

    id = db.Column(db.Integer, primary_key=True)
    district = db.Column(db.Unicode(100))
    normalized = db.Column(db.String(100))
    nuts = db.Column(db.String(20))
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


class NRPZS(db.Model):
    __tablename__ = 'nrpzs'

    id = db.Column(db.Integer, primary_key=True)

    misto_poskytovani_id = db.Column(db.Integer)
    zdravotnicke_zarizeni_id = db.Column(db.Integer)
    kod = db.Column(db.Integer)
    nazev_zarizeni = db.Column(db.Unicode(500))
    druh_zarizeni = db.Column(db.Unicode(500))
    obec = db.Column(db.Unicode(100))
    psc = db.Column(db.Integer)
    ulice = db.Column(db.Unicode(100))
    cislo_domovni_orientacni = db.Column(db.Unicode(10))
    kraj = db.Column(db.Unicode(100))
    kraj_code = db.Column(db.String(10))
    okres = db.Column(db.Unicode(100))
    okres_code = db.Column(db.String(10))
    spravni_obvod = db.Column(db.Unicode(100))
    ico = db.Column(db.Integer)
    typ_osoby = db.Column(db.Integer)
    pravni_forma_kod = db.Column(db.Integer)
    kraj_code_sidlo = db.Column(db.String(10))
    okres_code_sidlo = db.Column(db.String(10))
    obec_sidlo = db.Column(db.Unicode(100))
    psc_sidlo = db.Column(db.Integer)
    ulice_sidlo = db.Column(db.Unicode(100))
    cislo_domovni_orientacni_sidlo = db.Column(db.Integer)
    obor_pece = db.Column(db.Unicode(300))
    forma_pece = db.Column(db.Unicode(500))
    druh_pece = db.Column(db.Unicode(500))
    odborny_zastupce = db.Column(db.Unicode(200))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    last_access = db.Column(db.DateTime(timezone=True), default=func.now())


class Insurances(db.Model):
    __tablename__ = 'insurances'

    id = db.Column(db.Integer, primary_key=True)

    count = db.Column(db.Integer)
    expertise_name = db.Column(db.Unicode(100))
    expertise_code = db.Column(db.Integer)  # foreign key InsuranceCodes - code
    ico = db.Column(db.Integer)  # foreign key Ico
    insurance_company = db.Column(db.String(10))
    procedure_code = db.Column(db.Integer)
    region = db.Column(db.Unicode(10))  # cechy, morava, slezsko


class Doctors(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)

    doctor_id = db.Column(db.Unicode(100))
    university = db.Column(db.String(10))
    graduated_year = db.Column(db.Float)
    lifelong_studies = db.Column(db.Boolean)
    doctor_name = db.Column(db.Unicode(100))  # object
    doctor_url = db.Column(db.Unicode(200))   # object

    # TODO rozdelit?
    medical_specialty = db.Column(db.Unicode(100))
    private_practice = db.Column(db.Unicode(100))
    leading_doctor_licence = db.Column(db.Unicode(100))
    method_of_treatment_licence = db.Column(db.Unicode(100))  # object
    n_doctor_workplaces = db.Column(db.Integer)
    graduated_age_estimate = db.Column(db.Integer)
    age_estimate = db.Column(db.Float)
    workplace_name = db.Column(db.Unicode(100))   # object
    workplace_hospital_ward = db.Column(db.Unicode(100))  # object
    workplace_address = db.Column(db.Unicode(100))    # object
    zip_code = db.Column(db.Float)
    street = db.Column(db.Unicode(100))   # object
    city = db.Column(db.Unicode(100))     # object
    n_workplaces = db.Column(db.Float)
    n_doctors_in_workplace = db.Column(db.Float)
    workplace_url = db.Column(db.Unicode(100))    # object
    IC = db.Column(db.Unicode(100))   # object
    area = db.Column(db.Unicode(100))     # object

    district = db.Column(db.Unicode(100))
    nuts = db.Column(db.String(10))


class MedicalSpecialty(db.Model):
    __tablename__ = 'medicalspecialty'

    id = db.Column(db.Integer, primary_key=True)
    medical_specialty_name = db.Column(db.Unicode(50))
