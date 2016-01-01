import os

basedir = os.path.abspath(os.path.dirname(__file__))
print("BASEDIR: " + basedir)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'this-is-a-secret'

OAUTH_CREDENTIALS = {
    'facebook': {
        'id': os.environ.get('FACEBOOK_ID'),
        'secret': os.environ.get('FACEBOOK_SECRET')
    },
    'twitter': {
        'id': os.environ.get('TWITTER_ID'),
        'secret': os.environ.get('TWITTER_SECRET')
    }
}

# Mail server settings
MAIL_SERVER = 'mail.messagingengine.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# Admin list
ADMINS = ['jared@jaredharley.com']

# Pagination
POSTS_PER_PAGE = 3