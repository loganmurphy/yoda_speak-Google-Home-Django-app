# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

from google_yoda.settings.base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "DATABASE": "d154lfgjapcu2v",
        "DIALECT": "postgres",
        "HOST": "ec2-107-22-160-199.compute-1.amazonaws.com",
        "PORT": 5432,
    }
}
