# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

from google_yoda.settings.base import *
import dj_database_url

DATABASES['default'] =  dj_database_url.config()
