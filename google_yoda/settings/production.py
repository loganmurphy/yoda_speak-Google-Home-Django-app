# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

from google_yoda.settings.base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "name",
        "USER": "postgres",
        "PASSWORD": "pass",
        "HOST": "postgres://rdjlskrdbncwyp:d5197ce71d34d89d5ac1e2dc6a5278c6e92cba85c3255c708ffd8181ecb4c1a9@ec2-107-22-160-199.compute-1.amazonaws.com:5432/d154lfgjapcu2v",
        "PORT": 5432,
    }
}
