from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class BaseConfig:
    """Base configuration"""
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')
    WINES_PER_PAGE = 6
    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    TESTING = True
    TEMPLATES_AUTO_RELOAD = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
