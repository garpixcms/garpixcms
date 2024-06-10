import os
from environs import Env
from app.basedir import BASE_DIR
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from garpix_notify.settings import *  # noqa
from corsheaders.defaults import default_headers

env = Env()
env.read_env(os.path.join(BASE_DIR, '.env'), recurse=True)

ENABLE_GARPIX_AUTH = env.bool('ENABLE_GARPIX_AUTH', False)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', True)

API_URL = 'api'  # or api/v1, or api/v2, etc

ALLOWED_HOSTS = ['*']

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'tabbed_admin',
    'modeltranslation',
    'polymorphic_tree',
    'polymorphic',
    'mptt',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'django.contrib.sites',
    'solo',
    'fcm_django',
    'corsheaders',
    'rest_framework.authtoken',
    'oauth2_provider',
    'social_django',
    # garpixcms
    'garpix_utils',
    'eqator',
    'garpix_page',
    'garpix_menu',
    'garpix_notify',
    'garpix_package',
    'drf_spectacular',
    'garpix_user',
    'garpixcms',
    # website
    'app',
    'user',
    'garpix_admin_lock',
    'django.contrib.admin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'garpixcms.middleware.locale.GarpixLocaleMiddleware'
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
            os.path.join(BASE_DIR, '..', 'frontend', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'garpix_menu.context_processors.menu_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env.int('POSTGRES_PORT'),
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru'
USE_DEFAULT_LANGUAGE_PREFIX = False

LANGUAGES = (
    ('ru', 'Russian'),
)

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static-backend/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'public', 'static-backend')
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'public', 'media')

TEMPLATES_PATH = os.path.join(BASE_DIR, '..', 'frontend', 'templates')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '..', 'frontend', 'static'),
]

# ckeditor

CKEDITOR_UPLOAD_PATH = ''

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'width': '100%',
    },
}

# garpix page

COMMON_CONTEXT = 'garpix_page.contexts.default.context'

# menu

MENU_ICON_ALLOWED_TYPES = ['bmp', 'svg', 'jpg', 'png', 'jpeg']
MENU_ICON_MAX_SIZE = 1024 * 1024 * 1

MENU_TYPE_HEADER_MENU = 'header_menu'
MENU_TYPE_FOOTER_MENU = 'footer_menu'

MENU_TYPES = {
    MENU_TYPE_HEADER_MENU: {
        'title': 'Header menu',
    },
    MENU_TYPE_FOOTER_MENU: {
        'title': 'Footer menu',
    },
}

CHOICE_MENU_TYPES = [(k, v['title']) for k, v in MENU_TYPES.items()]

# Migrations

MIGRATION_MODULES = {
    'garpix_auth': 'app.migrations.garpix_auth',
    'garpix_user': 'app.migrations.garpix_user',
    'garpix_page': 'app.migrations.garpix_page',
    'garpix_menu': 'app.migrations.garpix_menu',
    'garpix_notify': 'app.migrations.garpix_notify',
    'garpixcms': 'app.migrations.garpixcms',
    'garpix_admin_lock': 'app.migrations.garpix_admin_lock'
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'

NOTIFY_SMS_URL = "http://sms.ru/sms/send"
NOTIFY_SMS_API_ID = env('NOTIFY_SMS_API_ID', "1234567890")
FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": env('FCM_SERVER_KEY', "1234567890")
}

# SPECTACULAR

SPECTACULAR_SETTINGS = {
    'TITLE': 'Application',
    'DESCRIPTION': '',
    'VERSION': '1.0.0',
}

# Celery

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')

# Celery
CELERY_BROKER_URL = 'redis://{}:6379/1'.format(REDIS_HOST)
CELERY_RESULT_BACKEND = 'redis://{}:6379/2'.format(REDIS_HOST)
# CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = TIME_ZONE
# CELERY_TASK_ALWAYS_EAGER = TEST
CELERY_ENABLE_UTC = False
DJANGO_CELERY_BEAT_TZ_AWARE = False

# Example notify

# notify events
EXAMPLE_EVENT = 1

NOTIFY_EVENTS = {
    EXAMPLE_EVENT: {
        'title': 'Example',
    },
}

CHOICES_NOTIFY_EVENT = [(k, v['title']) for k, v in NOTIFY_EVENTS.items()]

# Authentication

# GARPIX_ACCESS_TOKEN_TTL_SECONDS = 86400  # 24 hours
GARPIX_ACCESS_TOKEN_TTL_SECONDS = 0  # infinity
# GARPIX_REFRESH_TOKEN_TTL_SECONDS = 86400 * 14  # 14 days
GARPIX_REFRESH_TOKEN_TTL_SECONDS = 0  # infinity
DRFSO2_URL_NAMESPACE = 'drfso2'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'garpix_user.rest.authentication.MainAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

AUTHENTICATION_BACKENDS = [
    'garpix_user.utils.backends.CustomAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details'
)

if ENABLE_GARPIX_AUTH:
    AUTHENTICATION_BACKENDS += [
        'rest_framework_social_oauth2.backends.DjangoOAuth2',
    ]
    INSTALLED_APPS += [
        'rest_framework_social_oauth2',
        'garpix_auth',
    ]

GARPIX_PAGE_ADMIN_LIST_PER_PAGE = 25
GARPIX_PAGE_GLOBAL_CONTEXT = 'garpixcms.contexts.global_context.global_context'

# sentry
SENTRY_DSN_STRING = env('SENTRY_DSN_STRING', '')
if SENTRY_DSN_STRING != '':
    sentry_sdk.init(
        dsn=SENTRY_DSN_STRING,
        integrations=[DjangoIntegration()]
    )

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

GARPIXCMS_CELERY_SETTINGS = 'app.celery.app'

GARPIX_USER = {}

ENABLE_SWAGGER = False

CORS_ALLOW_HEADERS = list(default_headers) + [
    "user-session-token",
]

ISO_LOGS_NAME = 'garpixcms'

IB_ISO_LOGS_NAME = 'garpixcms_ib'
SYSTEM_ISO_LOGS_NAME = 'garpixcms_system'
