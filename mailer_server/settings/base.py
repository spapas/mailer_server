"""
Django settings for mailer_server project.
"""

import os
from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = '7x=ion&zd9%_hqv0)zc^rh6e#p$jw(8m#xqvt_viqb#fqv(n@+'
DEBUG = False
SITE_ID = 3

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'mailer_server.core',
    'mailer_server.tasks',
    'mailer_server.mail',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'compressor',
    'constance',
    'crispy_forms',
    'django_extensions',
    'django_filters',
    'django_rq',
    'django_tables2',
    'reversion',
    'rest_framework',
    'rest_framework.authtoken',
    'widget_tweaks',
    
]

MIDDLEWARE = [
    'reversion.middleware.RevisionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mailer_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mailer_server.core.context_processors.default_cp',
            ],
            'loaders': [
            ('django.template.loaders.cached.Loader', [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]),
        ],
        },
    },
]

WSGI_APPLICATION = 'mailer_server.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    }, {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }, {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    }, {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }
]

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/Athens'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = '/home/serafeim/mailer_server/static'
STATIC_URL = '/static_mailer_server/'
MEDIA_URL = '/media_mailer_server/'
MEDIA_ROOT = '/home/serafeim/mailer_server/media'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGIN_URL = '/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "unix://path/to/socket.sock?db=0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

RQ_QUEUES = {
    'default': {
        'USE_REDIS_CACHE': 'default',
    },
}

CACHE_MIDDLEWARE_KEY_PREFIX = 'mailer_server'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# SECURITY OPTIONS
SECURE_HSTS_SECONDS = 0
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True # Careful this allows session to work only on HTTPS on production
CSRF_COOKIE_SECURE = True # Careful this allows CSRF to work only on HTTPS on production
CSRF_COOKIE_HTTPONLY = True

ADMINS = MANAGERS = [('Serafeim Papastefanos', 'spapas@hcg.gr'), ]

# Default for django-filter
FILTERS_HELP_TEXT_EXCLUDE = True
FILTERS_HELP_TEXT_FILTER = False

# EMAIL cfg
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.hcg.gr'
MAIL_PORT = 587
EMAIL_HOST_USER = 'noreply@hcg.gr'
SERVER_EMAIL = 'noreply@hcg.gr'
EMAIL_HOST_PASSWORD = '' # Configure me in local.py
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@hcg.gr'

# crispy forms template pack
CRISPY_TEMPLATE_PACK = 'bootstrap3'

CONSTANCE_CONFIG = {
    'THE_ANSWER': (42, 'Answer to the Ultimate Question of Life, '
                       'The Universe, and Everything'),
}

CONSTANCE_REDIS_CONNECTION_CLASS = 'django_redis.get_redis_connection'
CONSTANCE_DATABASE_CACHE_BACKEND = 'default'

from .ldap_conf import *
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'mailer_server.core.auth.NoLoginModelBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

