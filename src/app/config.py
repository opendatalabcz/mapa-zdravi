class ConfigDB:
    SECRET_KEY = "46s85h4r5j4htdjhs4h56tjd4jnn8sdtj4d8m4d"
    # dialect+driver://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://mapazdravi_user:mapazdravi2022@db:5432/mapa_zdravi_web"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigDBdev:
    SECRET_KEY = "46s85h4r5j4htdjhs4h56tjd4jnn8sdtj4d8m4d"
    # dialect+driver://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://mapazdravi_user:mapazdravi2022@localhost:5432/mapa_zdravi_web"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
