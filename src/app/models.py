
from . import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # lowercase
# kraj = relationship("Kraj", back_populates="okresy") # uppercase, ve tride Okres
# Kraj.okresy = relationship("Okres", back_populates="kraj") # mimo tridu


# from sqlalchemy import Column, Integer, Unicode, DateTime, Boolean, Float, Date, ForeignKey, Index, ARRAY, Time


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


class NRPZS(db.Model):
    __tablename__ = 'NRPZS'

    mistoPoskytovaniId = db.Column(db.Integer)
    zdravotnickeZarizeniId = db.Column(db.Integer)
    kod = db.Column(db.Integer, primary_key=True)
    nazevZarizeni = db.Column(db.Unicode(500))
    druhZarizeni = db.Column(db.Unicode(500))
    obec = db.Column(db.Unicode(100))
    psc = db.Column(db.Integer)
    ulice = db.Column(db.Unicode(100))
    cisloDomovniOrientacni = db.Column(db.Unicode(10))
    kraj = db.Column(db.Unicode(100))
    krajCode = db.Column(db.String(10))
    okres = db.Column(db.Unicode(100))
    okresCode = db.Column(db.String(10))
    spravniObvod = db.Column(db.Unicode(100))
    poskytovatelTelefon = db.Column(db.String(100))
    poskytovatelFax = db.Column(db.String(100))
    poskytovatelEmail = db.Column(db.String(100))
    poskytovatelWeb = db.Column(db.String(100))
    ico = db.Column(db.Integer)
    typOsoby = db.Column(db.Integer)
    pravniFormaKod = db.Column(db.Integer)
    krajCodeSidlo = db.Column(db.String(10))
    okresCodeSidlo = db.Column(db.String(10))
    obecSidlo = db.Column(db.Unicode(100))
    pscSidlo = db.Column(db.Integer)
    uliceSidlo = db.Column(db.Unicode(100))
    cisloDomovniOrientacniSidlo = db.Column(db.Integer)
    oborPece = db.Column(db.Unicode(300))
    formaPece = db.Column(db.Unicode(500))
    druhPece = db.Column(db.Unicode(500))
    odbornyZastupce = db.Column(db.Unicode(200))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    last_access = db.Column(db.DateTime(timezone=True), default=func.now())


class InsuranceCodes(db.Model):
    __tablename__ = 'Zdravotnické kódy'

    code = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100))
    rank = db.Column(db.Integer)
    value = db.Column(db.Float)  # sazba rezie


class Insurances(db.Model):
    __tablename__ = 'Zdravotnické výkony'

    id = db.Column(db.Integer, primary_key=True)

    count = db.Column(db.Integer)
    expertise = db.Column(db.Integer)  # foreign key InsuranceCodes - code
    facilities_id = db.Column(db.Integer)  # foreign key Ico
    insurance_company = db.Column(db.String(10))
    procedure_code = db.Column(db.Integer)
    region = db.Column(db.Unicode(10))  # cechy, morava, slezsko


class Doctors(db.Model):
    __tablename__ = 'Lékaři'

    # TODO primary key

    # TODO , primary_key=True
    _id = db.Column(db.Unicode(100), primary_key=True)
    university = db.Column(db.String(10))
    graduated_year = db.Column(db.Integer)   # float64
    lifelong_studies = db.Column(db.Boolean)
    doctor_name = db.Column(db.Unicode(100))  # object
    doctor_url = db.Column(db.Unicode(200))   # object

    # TODO rozdelit?
    medical_specialty = db.Column(db.Unicode(100))
    private_practice = db.Column(db.Unicode(100))
    leading_doctor_licence = db.Column(db.Unicode(100))
    method_of_treatment_licence = db.Column(db.Unicode(100))  # object
    n_doctor_workplaces = db.Column(db.Unicode(100))  # int64
    graduated_age_estimate = db.Column(db.Unicode(100))   # int64
    age_estimate = db.Column(db.Unicode(100))     # float64
    workplace_name = db.Column(db.Unicode(100))   # object
    workplace_hospital_ward = db.Column(db.Unicode(100))  # object
    workplace_address = db.Column(db.Unicode(100))    # object
    zip_code = db.Column(db.Unicode(100))     # float64
    street = db.Column(db.Unicode(100))   # object
    city = db.Column(db.Unicode(100))     # object
    n_workplaces = db.Column(db.Unicode(100))     # float64
    n_doctors_in_workplace = db.Column(db.Unicode(100))   # float64
    workplace_url = db.Column(db.Unicode(100))    # object
    IC = db.Column(db.Unicode(100))   # object
    area = db.Column(db.Unicode(100))     # object

    # TODO vyklestit workspaces, jejich obory atd
    # TODO odstranit camelcase
    # TODO pridat relations
