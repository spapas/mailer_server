import logging
from .base import *

DEBUG = True
SITE_ID = 1


INSTALLED_APPS += (
    'debug_toolbar',
)
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = ['127.0.0.1', ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

TEMPLATES[0]['OPTIONS']['loaders'] = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATES[0]['OPTIONS']['debug'] = True

AUTHENTICATION_BACKENDS = (
#     'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

CSRF_COOKIE_SECURE = False # Override CSRF to work also with http
SESSION_COOKIE_SECURE = False # Override session to work also with http

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mailer_server',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'db',
        'PORT': '',
    }
}

SECRET_KEY = '111222333overrideme1298mailer_server031892jklaksdiasdlkajsdlkasjmailer_serverdlkdfgdfg'

try:
    from .local import *
    from .ldap_conf import *

    logger = logging.getLogger('django_auth_ldap')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
except:
    pass

MAGIC_FILE_PATH = 'c:/util/magic_file'
