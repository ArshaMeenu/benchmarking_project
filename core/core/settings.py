import os.path
from pathlib import Path
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-1tt%##x6%pq8nly$zm&=e3=&terovpoa$ophchk36aak!q8!z5"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party
    'crispy_forms',
    'debug_toolbar',
    'captcha',
    'multiselectfield',
    'cities_light',

    # apps
    'emailattach',
    'djangobaseviews',
    'djangogenericviews',
    'complexqueries',
    'modelrelationship',
    'mastering_django',

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # for debug tooler
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# for debug tooler

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            # while using myfilters.py for add custom class like addclass in forms
            'libraries': {
                'myfilters': 'mastering_django.templatetags.myfilters',

            }
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    'mastering_django': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mastering_django',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/'),
]

MEDIA_URL = '/media/'  # The URL endpoint is specified here. This is the URL where the user can upload their files
# from their browser.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # defines the root path where the file will be saved.

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email using sendgrid
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIT_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = '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'
#

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "arsha@sayonetech.com"
EMAIL_HOST_PASSWORD = '928@sayone'
DEFAULT_FROM_EMAIL = "arsha@sayonetech.com"

# Django Crispy package
# CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'mastering_django.CustomUser'  ### this for mastering_django's customer model

# recaptcha config
RECAPTCHA_PUBLIC_KEY = '6LezoDInAAAAAAw8Pq3HrexXC4Q6eTFTHp5YvFTd'
RECAPTCHA_PRIVATE_KEY = '6LezoDInAAAAANu1UII0I8DmcMd3glWPWUX5-7or'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

# LOGIN URLs
LOGIN_URL = 'mastering_django:login'
LOGIN_REDIRECT_URL = 'mastering_django:index-function-view'
LOGOUT_REDIRECT_URL = 'mastering_django:index-function-view'

MESSAGE_TAGS = {
    messages.ERROR: 'danger'  # here we can override tags meaning in place of there actual color replace by another
}

# PAYMENT GATEWAY SETTINGS
RAZORPAY_KEY_ID = 'rzp_test_XoxDlCxqzVtN7E'
RAZORPAY_KEY_SECRET = 'OxfQbxinLYiZiUQq6ksXbRaN'
