import os

class ConfigDB:
    SECRET_KEY = os.environ["SECRET_KEY"]
    # dialect+driver://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:5432/{os.environ['POSTGRES_DB']}"
        
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ConfigDBdev:
    SECRET_KEY = os.environ["SECRET_KEY"]
    # dialect+driver://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:5432/{os.environ['POSTGRES_DB']}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
