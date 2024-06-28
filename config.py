import os
from dotenv import load_dotenv

# Takes the location of the database
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


# Settings
# class Config(object):
class Config(object):

    # DO NOT use "DEBUG = True" in production environments
    DEBUG = True

    # DO NOT use Unsecure Secrets in production environments
    # Generate a safe one with:
    #    python -c "import os; print(repr(os.urandom(24)));"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SECURITY_URL_PREFIX = "/admin"

    # ADMINS = ['your-email@example.com']
    ADMINS = [
        '"Admin One" <admin1@gmail.com>',
    ]
    # Index
    WODS_PER_PAGE = 1