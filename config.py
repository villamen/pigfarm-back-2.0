import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_secreta_para_jwt'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:5831202@localhost/pigfarm'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3307/pigfarm'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
