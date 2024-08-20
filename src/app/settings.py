"""
Django settings for mimosa project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import socket
from distutils.util import strtobool
from pathlib import Path

import stripe

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = bool(strtobool(os.getenv("DEBUG", "false")))

# https://docs.djangoproject.com/en/5.0/ref/settings/#std:setting-ALLOWED_HOSTS
allowed_hosts = os.getenv("ALLOWED_HOSTS", ".localhost,127.0.0.1,[::1]")
ALLOWED_HOSTS = list(map(str.strip, allowed_hosts.split(",")))

# Application definitions
INSTALLED_APPS = [
    "core.apps.CoreConfig",
    "debug_toolbar",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

# Starting with Django 4.1+ we need to pick which template loaders to use
# based on our environment since 4.1+ will cache templates by default.
default_loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

cached_loaders = [("django.template.loaders.cached.Loader", default_loaders)]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.settings",
            ],
            "loaders": default_loaders if DEBUG else cached_loaders,
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "mimosa"),
        "USER": os.getenv("POSTGRES_USER", "mimosa"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
        "HOST": os.getenv("POSTGRES_HOST", "postgres"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator"
        # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "MinimumLengthValidator"
        # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".CommonPasswordValidator"
        # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".NumericPasswordValidator"
        # noqa: E501
    },
]

# Sessions
# https://docs.djangoproject.com/en/5.0/ref/settings/#sessions
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Caching
# https://docs.djangoproject.com/en/5.0/topics/cache/
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

# Celery
# https://docs.celeryproject.org/en/stable/userguide/configuration.html
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = "/uploads/"
MEDIA_ROOT = os.path.join(BASE_DIR, "..", "uploads")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "..", "public")]
STATIC_ROOT = os.path.join(BASE_DIR, "..", "public_collected")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Django Debug Toolbar
# https://django-debug-toolbar.readthedocs.io/
if DEBUG:
    # We need to configure an IP address to allow connections from, but in
    # Docker we can't use 127.0.0.1 since this runs in a container but we want
    # to access the toolbar from our browser outside of the container.
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "10.0.2.2",
        os.environ.get("INTERNAL_IP", "127.0.0.1"),
    ]

# Stripe.
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")
STRIPE_API_BASE = os.environ.get("STRIPE_API_BASE")
STRIPE_CURRENCY = "aud"

# Set the key and base so that it doesn't need to be set in each file.
stripe.api_key = STRIPE_SECRET_KEY
stripe.api_base = STRIPE_API_BASE

# Site.
SITE_PROTOCOL = os.environ.get("SITE_PROTOCOL")
SITE_DOMAIN = os.environ.get("SITE_DOMAIN")
SITE_PORT = int(os.environ.get("SITE_PORT"))

# Email settings
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("EMAIL_HOST")
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
    EMAIL_USE_TLS = bool(strtobool(os.environ.get("EMAIL_USE_TLS", "true")))
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
