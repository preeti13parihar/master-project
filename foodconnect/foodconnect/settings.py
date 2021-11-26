import os
import logging
import json
from urllib import request
from pathlib import Path
from datetime import timedelta
import pymysql
import numpy as np
import pandas as pd
import pickle
import scipy
pymysql.install_as_MySQLdb()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r8mzzw8s#z01iv8_mn3udrvnnr^2=%r-a#@am5(k+)%_20quu+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOWED_ORIGINS = True
CORS_ALLOW_ALL_ORIGINS= True

# Application definition
URL_PREFIX = "app/"
LOGIN_REDIRECT_URL = "foodzone/home"

AUTH_USER_MODEL = 'authentication.User'

APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID", None)
APP_SECRET_KEY = os.getenv("COGNITO_APP_CLIENT_SECRET", None)
COGNITO_POOL_ID = os.getenv("COGNITO_USER_POOL_ID", None)
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)
AWS_REGION = os.getenv("AWS_REGION", None)
S3_BUCKET = os.getenv("S3_BUCKET", None)
S3_FILE_URL = f"http://s3-{AWS_REGION}.amazonaws.com/{S3_BUCKET}/"
DB_NAME = os.getenv("DB_NAME", None)
DB_USERNAME = os.getenv("DB_USERNAME", None)
DB_PASSWORD = os.getenv("DB_PASSWORD", None)
HOST = os.getenv("HOST", "127.0.0.1")
PORT = os.getenv("PORT", 9091)
ENV = os.getenv("ENV", "local")
LOG_LEVEL = os.getenv("LOG_LEVEL", logging.INFO)
SESSION_COOKIE_DOMAIN = os.getenv("SESSION_COOKIE_DOMAIN", "localhost")
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", True)
SESSION_COOKIE_EXPIRY = os.getenv("SESSION_COOKIE_EXPIRY", 1)

if not APP_CLIENT_ID:
    print("Please set COGNITO_APP_CLIENT_ID !!!")
elif not APP_SECRET_KEY:
    print("Please set COGNITO_APP_CLIENT_SECRET !!!")
elif not COGNITO_POOL_ID:
    print("Please set COGNITO_USER_POOL_ID !!!")
elif not AWS_ACCESS_KEY:
    print("Please set AWS_ACCESS_KEY_ID !!!")
elif not APP_SECRET_KEY:
    print("Please set AWS_SECRET_ACCESS_KEY !!!")
elif not AWS_REGION:
    print("Please set AWS_REGION !!!")
elif not S3_BUCKET:
    print("Please set S3_BUCKET !!!")
elif not DB_NAME:
    print("Please set DB_NAME !!!")
elif not DB_USERNAME:
    print("Please set DB_USERNAME !!!")
elif not DB_PASSWORD:
    print("Please set DB_PASSWORD !!!")

from utils import log
log.validate_log_level(LOG_LEVEL)

HTTP_ONLY_COOKIE = True
USE_CSRF = False
AUTO_CREATE_USER = True
SECURE_COOKIE = True
APPEND_SLASH=True

CORS_WHITELIST_FILEPATH = os.getenv("CORS_WHITELIST_FILEPATH", "./cors.list")

INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',

'core',
'trail',
'reviews',
'foodzone',
'friends',
'friendship',
'authentication',
'rest_framework',
'corsheaders'
]

MIDDLEWARE = [
'corsheaders.middleware.CorsMiddleware',
'django.middleware.security.SecurityMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
# 'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',

# 'django.contrib.auth.middleware.AuthenticationMiddleware',
# 'django.contrib.auth.middleware.RemoteUserMiddleware',
'authentication.middleware.cognito_django_middleware.AwsDjangoMiddleware',
]
AUTHENTICATION_BACKENDS = [
# 'django.contrib.auth.backends.RemoteUserBackend',
# 'django.contrib.auth.backends.ModelBackend',
'authentication.middleware.cognito_rest_authentication.AwsRestAuthentication'
]

REST_FRAMEWORK = {
'DEFAULT_PERMISSION_CLASSES': (
'core.api.permissions.DenyAny',
),
'DEFAULT_AUTHENTICATION_CLASSES': (
'authentication.middleware.cognito_rest_authentication.AwsRestAuthentication',

# 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
# 'rest_framework_simplejwt.authentication.JWTAuthentication'
),
}

ROOT_URLCONF = 'foodconnect.urls'

TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [],
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

CORS_ALLOW_HEADERS = [
'accept',
'accept-encoding',
'authorization',
'content-type',
'dnt',
'origin',
'user-agent',
'x-csrftoken',
'x-requested-with',
'accesstoken',
'refreshtoken',
'access-control-allow-origin',
'access-control-allow-headers'
]

WSGI_APPLICATION = 'foodconnect.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.mysql',
'NAME': DB_NAME,
'USER': DB_USERNAME,
'PASSWORD': DB_PASSWORD,
'HOST': HOST, # Or an IP Address that your DB is hosted on
'PORT': '3306',
'OPTIONS': {
'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
}
}
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True


USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_URL='/static/'
ML_URL = os.path.join(BASE_DIR, 'foodconnect/static/')

KNN=pickle.load(open(ML_URL+'foodconnect/KNNModel', 'rb'))
LE=pickle.load(open(ML_URL+'foodconnect/LabelEncoder', 'rb'))
CSR=scipy.sparse.load_npz(ML_URL+'foodconnect/sparse_matrix.npz')