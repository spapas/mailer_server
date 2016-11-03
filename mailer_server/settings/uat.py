from .base import *

DEBUG = False
SITE_ID = 2

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

CSRF_COOKIE_SECURE = False # Override CSRF to work also with http
SESSION_COOKIE_SECURE = False # Override session to work also with http

try:
    from .local import *
except ImportError:
    pass
