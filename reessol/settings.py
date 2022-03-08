"""
Django settings for reessol project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
import sys
from django.core.management.utils import get_random_secret_key
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS",
    "127.0.0.1,localhost,https://ressol.vercel.app/,https://reessol-backend-new-zbsfa.ondigitalocean.app",
).split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Third Party Apps
    ## REST
    "rest_framework",
    # CORS
    "corsheaders",
    # Images
    "versatileimagefield",
    # Filters
    "django_filters",
    ## Auth
    "rest_framework.authtoken",
    "dj_rest_auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    # Custom Apps
    "apps.profiles",
    "apps.properties",
    "apps.payments",
    "apps.messaging",
]

SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = "none"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# STATIC_URL = "/static/"
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# STATIC_ROOT = os.path.join(BASE_DIR, "assests")


VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    "product_headshot": [
        ("full_size", "url"),
        ("thumbnail", "thumbnail__100x100"),
        ("medium_square_crop", "crop__400x400"),
        ("small_square_crop", "crop__50x50"),
    ]
}
REFERRER_POLICY = "no-referrer"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Third Party
    ## CORS
    "corsheaders.middleware.CorsMiddleware",
    "django_referrer_policy.middleware.ReferrerPolicyMiddleware",
]

ROOT_URLCONF = "reessol.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "reessol.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

if DEVELOPMENT_MODE is True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != "collectstatic":
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
    }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True
RAZOR_KEY_ID = "rzp_test_fZKYjMuBhXDFuk"
RAZOR_KEY_SECRET = "NZKM6V0kgO4rpTvcGeFCXkSV"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS Settings

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://reessol.vercel.app",
    "https://reessol-backend-new-zbsfa.ondigitalocean.app",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    "http://localhost:3000",
    "https://reessol.vercel.app",
    "https://reessol-backend-new-zbsfa.ondigitalocean.app",
]

CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "https://reessol.vercel.app",
    "https://reessol-backend-new-zbsfa.ondigitalocean.app",
)

TWILIO_ACCOUNT_SID = "AC24d867a57956cc50c13485855be16f80"
TWILIO_AUTH_TOKEN = "cffef1ee6fa1ae861d1f2ef1d1b1a52f"

# TWILIO_ACCOUNT_SID = "AC9c4ca64a1177382f4fc0162a3d11a31d"
# TWILIO_AUTH_TOKEN = "5977d694abfaf80a3a3aced4af3718dc"
# TWILIO_NUMBER = "+19036626716"
TWILIO_NUMBER = "+19106346054"
