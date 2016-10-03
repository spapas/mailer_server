import logging
from .base import *

DEBUG = True
SITE_ID = 1


INSTALLED_APPS += (
    'debug_toolbar',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

TEMPLATES[0]['OPTIONS']['loaders'] = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

AUTHENTICATION_BACKENDS += (
    'django.contrib.auth.backends.ModelBackend',
)

CSRF_COOKIE_SECURE = False # Override CSRF to work also with http
SESSION_COOKIE_SECURE = False # Override session to work also with http

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

try:
    from .local import *
except ImportError as e:
    print e
    
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG) 
