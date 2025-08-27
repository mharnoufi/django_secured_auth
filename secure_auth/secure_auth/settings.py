from pathlib import Path
import os

DJANGO_SECURE = os.getenv("DJANGO_SECURE", "false").lower() == "true"

AUTH_USER_MODEL = "accounts.User"

# Backend qui bloque les comptes verrouillés (email reste l'identifiant)
AUTHENTICATION_BACKENDS = [
    "accounts.backends.EmailBackend",
]

# Argon2 en hasher principal
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    # "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    # "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    # "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Sessions sécurisées
SESSION_COOKIE_AGE = 3600  # 1 heure
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = DJANGO_SECURE
CSRF_COOKIE_SECURE = DJANGO_SECURE

# Redirection automatique HTTP -> HTTPS
SECURE_SSL_REDIRECT = DJANGO_SECURE

# HSTS (strict transport security)
SECURE_HSTS_SECONDS = 31536000 if DJANGO_SECURE else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = DJANGO_SECURE

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-x619a71*gkb+(#qpwj4jgw^9^+w#&267028596@ga%)0g%rq0m"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not DJANGO_SECURE

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts.apps.AccountsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "secure_auth.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "secure_auth.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
