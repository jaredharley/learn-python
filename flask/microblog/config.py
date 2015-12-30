import os

basedir = os.path.abspath(os.path.dirname(__file__))
print("BASEDIR: " + basedir)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'this-is-a-secret'

OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '1234567',
        'secret': '12345678901234567890'
    },
    'twitter': {
        'id': 'YLEYxzqfC8OqY4QMWeVEysNDx',
        'secret': '85Y7LvrZhbigiM6rMOx0iXYsYzl97nEAip7opdYpsZ88okcIo6'
    }
}

# Mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# Admin list
ADMINS = ['jared@jaredharley.com']