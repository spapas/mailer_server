from .base import *

# These should be imprted from from base.py but I'll redefine them for clarity
DEBUG = False
SITE_ID = 1
COMPRESS_OFFLINE = True

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic', )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware', )

# I recommend disabling these for production
CSRF_COOKIE_SECURE = False # Override CSRF to work also with http
SESSION_COOKIE_SECURE = False # Override session to work also with http


from .local import *
    
from .ldap_conf import *



AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'mailer_server.core.auth.NoLoginModelBackend',
)