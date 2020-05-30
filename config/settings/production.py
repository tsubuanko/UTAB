from .common import *

DEBUG = False

ALLOWED_HOSTS = [
    'Utab-env.eba-ue4s4zg3.us-east-1.elasticbeanstalk.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')