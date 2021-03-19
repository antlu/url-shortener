import os

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ImproperlyConfigured(Exception):
    pass

class BaseConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DB_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DB_URL') or 'sqlite://'

class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DB_URL')

config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
}
