from .base import *

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'tasma',
        'USER':     'postgres',
        'PASSWORD': 'q1w2e3r4',
        'HOST':     '10.0.3.17',
        'PORT':     '5432'
    }
}