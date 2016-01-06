import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_LOC = os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLALCHEMY_DATABASE_LOC
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True
SECRET_KEY = 'this-is-a-secret'