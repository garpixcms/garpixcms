import os
from pathlib import Path
from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', True)

ALLOWED_HOSTS = ['*']

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'polymorphic_tree',
    'polymorphic',
    'mptt',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'django.contrib.sites',
    'app',
    'garpix_qa',
    'garpix_page',
    'garpix_menu',
    'garpixcms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'public', 'static')
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
    'garpix_page': 'app.migrations.garpix_page',
    'garpix_menu': 'app.migrations.garpix_menu',
    'garpixcms': 'app.migrations.garpixcms',
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
