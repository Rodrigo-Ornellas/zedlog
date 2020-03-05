"""
Django settings for zim project.

Generated by 'django-admin startproject' using Django 1.11.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""


import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=-)ko^vj*9hy3b7k3-6krlb7jn*t75^o=h$x&*_p4uq($bg5!c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Original ALLOWED_HOSTS - commented out and replaced by new command on the bottom of the page
# ALLOWED_HOSTS = []


# Application definition

# Use Whitenoise to serve STATIC files in the DEV environment
# http://whitenoise.evans.io/en/stable/django.html#runserver-nostatic
# https://docs.djangoproject.com/en/3.0/ref/contrib/staticfiles/#cmdoption-runserver-nostatic
# INSTALLED_APPS = [ 'whitenoise.runserver_nostatic',

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'valdata',
    'schedule'
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zim.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
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

WSGI_APPLICATION = 'zim.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Media Files
# https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-MEDIA_ROOT

MEDIA_ROOT = os.path.join(BASE_DIR, 'www' , 'media')

MEDIA_URL = '/media/'


# https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-DATETIME_INPUT_FORMATS
DATETIME_INPUT_FORMATS = [
    '%d-%m-%Y %H:%M:%S',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'


# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication
# https://wsvincent.com/django-user-authentication-tutorial-login-and-logout/
# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# ==================================================================================================
# this sends the emails to the CONSOLE
# https://docs.djangoproject.com/en/3.0/topics/email/
# ==================================================================================================
if (DEBUG == True):
    # this will send the email to the console
    # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    # this will SAVE the emails to a FILE/FOLDER in the backend of the DJANGO project
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")


# https://wsvincent.com/django-referencing-the-user-model/
# AUTH_USER_MODEL = 'users.CustomUser'

# ==================================================================================================
# HEROKU DEPLOY CONFIGURATION
# ==================================================================================================
# instructions for the deploy
# https://www.codementor.io/@jamesezechukwu/how-to-deploy-django-app-on-heroku-dtsee04d4
# https://simpleisbetterthancomplex.com/tutorial/2016/08/09/how-to-deploy-django-applications-on-heroku.html


# Static files (CSS, JavaScript, Images)
# If you have files currently in your STATIC_ROOT that you wish to serve then you need 
# to move these to a different directory and put that other directory in STATICFILES_DIRS. 
# Your STATIC_ROOT directory should be empty and all static files should be collected 
# into that directory (i.e., it should not already contain static files)

# STATIC_ROOT is the path of the folder where the compiled files will be served from after collectstatic
# command = python manage.py collectstatic # this command will compile all the STATIC files into this folder.
STATIC_ROOT = os.path.join(BASE_DIR, 'www')

# Extra lookup directories for collectstatic to find static files
# when configured, COLLECTSTATIC complains of duplicate files
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'valdata', 'static'),
# )

if (DEBUG == False):

    # Current Virtual Env App configuration
    # pip freeze > requirements.txt

    # Heroku Commands
    #   0) Push the code to Heroku Deployment
    #   git push heroku master
    
    #   1) Test Heroku Locally - starts a local server
    #   heroku local web

    #   1a) Open Live Site
    #   heroku open

    #   2) Provides info about remote heroku database
    #   heroku pg:info

    #   3) Read End of Log files
    #   heroku logs --tail
    #   heroku logs -p postgres -t

    #   4) Heroku Addons
    #   heroku addons
    
    #   5) Heroku Live Database
    #   heroku addons:create heroku-postgresql:hobby-dev

    #   6) Managing Heroku Configuration Variables
    #   heroku config

    # Configure Django App for Heroku.
    # https://github.com/heroku/django-heroku
    import django_heroku
    django_heroku.settings(locals())


    #  Add configuration for static files storage using whitenoise
    # from Coding for Entrepreneurs Tutorial
    # STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
    # the above value is not compatible with WhiteNoise 4.0 - use the below code
    # https://stackoverflow.com/questions/55813584/django-whitenoise-configuration-is-incompatible-with-whitenoise-v4-0
    # http://whitenoise.evans.io/en/stable/changelog.html#v4-0
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    

    # Update Database Configuration in settings.py
    import dj_database_url
    prod_db = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(prod_db)

    ALLOWED_HOSTS = ['https://zedlog.herokuapp.com/']