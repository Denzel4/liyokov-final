import datetime
import os

from logging.config import fileConfig

basedir = os.path.abspath(os.path.dirname(__file__))
mysql_local_base = 'mysql+pymysql://macula:macula@localhost/'
database_name = 'macula'


class BaseConfig:
    """Base configuration."""
    FIXTURES_DIRS = './project/server/fixtures/'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=0, minutes=60)
    JWT_SECRET_KEY = os.getenv('SECRET_KEY', '\xdf-vm"\xadv-\xa8\xff\xc7\xe1\xc3\x05E\xe3\x14\x8f;\x06\xbb\xbf\xae.')
    SECRET_KEY = os.getenv('SECRET_KEY', '\xdf-vm"\xadv-\xa8\xff\xc7\xe1\xc3\x05E\xe3\x14\x8f;\x06\xbb\xbf\xae.')
    SECURITY_PASSWORD_SALT = os.getenv('SECRET_KEY', '\xdf-vm"\xadv-\xa8\xff\xc7\xe1\xc3\x05E\xe3\x14\x8f;\x06\xbb\xbf\xae.')
    JWT_IDENTITY_CLAIM = 'sub'
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_NAME = 'Macula'
    LOGGING = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'formatter': 'default',
                'filename': './project/server/logs/application.log'
            }
        },
        'loggers': {
            'MACULA': {
                'level': 'ERROR',
                'handlers': ['file'],
                'propagate': True,
                'qualname': 'macula.error'
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }

    # gmail authentication
    MAIL_USERNAME = os.getenv('APP_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('APP_MAIL_PASSWORD')
    # SET GLOBAL FOREIGN_KEY_CHECKS=0;
    API_AWS_ACCESS_KEY_ID = os.getenv('API_AWS_ACCESS_KEY_ID')
    API_AWS_SECRET_ACCESS_KEY = os.getenv('API_AWS_SECRET_ACCESS_KEY')

    # LOGGER
    # fileConfig(basedir + '/logging.conf')

    # Dataset directory

    PATH_DIR = 'paths.conf'



class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = mysql_local_base + database_name
    MAIL_DEFAULT_SENDER = 'macula@creationauts.com'

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # mail accounts
    MAIL_DEFAULT_SENDER = 'macula@creationauts.com'

    # UI Route
    UI_URL = 'http://macula.com/'


class TestingConfig(BaseConfig):
    """Testing configuration."""
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=0, seconds=5)
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = mysql_local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql:///example'
