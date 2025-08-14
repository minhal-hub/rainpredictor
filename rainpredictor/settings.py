import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load config.json (local, not committed)
CONF = {}
CONFIG_PATH = BASE_DIR / 'config.json'
if CONFIG_PATH.exists():
    with open(CONFIG_PATH, 'r') as fh:
        CONF = json.load(fh)

SECRET_KEY = CONF.get('SECRET_KEY', 'dev-unsafe-secret-key')
DEBUG = bool(CONF.get('DEBUG', True))
ALLOWED_HOSTS = CONF.get('ALLOWED_HOSTS', ['*'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'prediction',
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

ROOT_URLCONF = 'rainpredictor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rainpredictor.wsgi.application'

# PostgreSQL via config.json
DATABASES = {
    'default': {
        'ENGINE': CONF.get('DATABASE', {}).get('ENGINE', 'django.db.backends.postgresql'),
        'NAME': CONF.get('DATABASE', {}).get('NAME', 'rainpredictor'),
        'USER': CONF.get('DATABASE', {}).get('USER', 'postgres'),
        'PASSWORD': CONF.get('DATABASE', {}).get('PASSWORD', ''),
        'HOST': CONF.get('DATABASE', {}).get('HOST', '127.0.0.1'),
        'PORT': CONF.get('DATABASE', {}).get('PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

LOGIN_REDIRECT_URL = 'prediction:index'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
