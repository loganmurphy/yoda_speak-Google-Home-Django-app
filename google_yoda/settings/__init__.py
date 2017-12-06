import os

ENVIRONMENT = os.environ.get('ENVIRONMENT', '')

if ENVIRONMENT:
    print("Loading {} Settings".format(ENVIRONMENT.upper()))

else:
    print("Unknown ENV Loading DEVELOPMENT Settings")

if ENVIRONMENT == 'production':
    from google_yoda.settings.production import *

else:
    from google_yoda.settings.development import *
