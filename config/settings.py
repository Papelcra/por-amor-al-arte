"""
Django settings for config project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# ====================== 🔐 SEGURIDAD ======================

SECRET_KEY = 'django-insecure--6q=w*7=7^(gh^a3s2lm53e289#hr^kbzuqr-3f$llhygkrz7h'
DEBUG = True
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Esto permite que los formularios funcionen en el dominio de Render
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://por-amor-al-arte.onrender.com' # Cambia esto por tu URL real de Render
]


# ====================== 📦 APLICACIONES ======================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',

    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Apps propias
    'users',
    'artists.apps.ArtistsConfig',
    'groups',
    'catalog',
    'core',
    'dashboard',

    # Extras
    'widget_tweaks',
]

SITE_ID = 1


# ====================== ⚙️ MIDDLEWARE ======================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <--- WhiteNoise siempre aquí arriba
    'django.contrib.sessions.middleware.SessionMiddleware', # <--- ESTA ES LA QUE FALTA
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # <--- Sesiones debe ir ANTES que esta
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Si usas allauth para Google, asegúrate de tener esta también:
    'allauth.account.middleware.AccountMiddleware', 
]


# ====================== 🔗 URLS ======================

ROOT_URLCONF = 'config.urls'


# ====================== 🧠 TEMPLATES ======================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # requerido por allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ====================== 🚀 WSGI ======================

WSGI_APPLICATION = 'config.wsgi.application'


# ====================== 🗄️ BASE DE DATOS ======================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ====================== 👤 USUARIO ======================

AUTH_USER_MODEL = 'users.User'


# ====================== 🔑 PASSWORD ======================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
]

# ====================== 🌍 INTERNACIONALIZACIÓN ======================

LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True


# ====================== 📁 STATIC ======================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ====================== 📂 MEDIA ======================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ====================== 🔐 AUTH ======================

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'


# ====================== 📨 ALLAUTH ======================

ACCOUNT_SIGNUP_FORM_CLASS = 'users.forms.CustomSignupForm'

ACCOUNT_ADAPTER = 'users.adapter.MyAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'users.adapter.MySocialAccountAdapter'  # ← agrega esta línea
ACCOUNT_LOGIN_METHODS = {'email', 'username'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'optional'


# 🔥 AQUÍ ESTÁ LA CLAVE DE TU PROBLEMA (REDIRECCIÓN POR ROL)
ACCOUNT_ADAPTER = 'users.adapter.MyAccountAdapter'


# ====================== 📧 EMAIL ======================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ====================== 🌐 GOOGLE ======================

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'