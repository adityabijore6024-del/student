"""
Django settings for course project.
"""

from pathlib import Path
import os
import dj_database_url

# 1. Sabse pehle BASE_DIR aayega
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
# (Ab Railway se automatic SECRET_KEY lega)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-$-$q(@$@bz+31i!e&h%5r_f&o2n0*vgwpospn@gdx68#9c@g+-')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']  # '*' ka matlab hai ye kisi bhi domain par chal jayega
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # CSS/JS handle karne ke liye
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'course.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'course.wsgi.application'


# 2. Database Setting (Sirf ek baar aayega)
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}",
        conn_max_age=500
    )
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# 3. Yahan saari Static File settings theek kardi hain
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Railway ko yahan files milengi
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'frontend', 'static')]


RAZORPAY_KEY_ID = "rzp_test_Sy5GCNmQyyzAKR"
RAZORPAY_KEY_SECRET = "S2M9pvOT4DlbYhilyMJUNf05"

GEMINI_API_KEY = "AQ.Ab8RN6Iy22GtCJJPiGZan81dURKxqA4qPIM5ISIEo9FpN4Z95A"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
