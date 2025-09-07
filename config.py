import os

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_secreta_para_jwt'
#     # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:5831202@localhost/pigfarm'
#    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3307/pigfarm'
#     SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:5831202@localhost:5432/pigfarm'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_secreta_para_jwt'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # <-- aquí el cambio

    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        # Render a veces entrega "postgres://" y SQLAlchemy necesita "postgresql://"
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

