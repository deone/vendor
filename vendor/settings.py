"""
Django settings for vendor project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sz%v&-pi15-+u&501z&!8jjo2v*i3a-fd9^&!6iyadp$y(b7#j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['vendor-deone.c9users.io']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'vend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'vendor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'vendor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vendor',
        'USER': 'vendor',
        'PASSWORD': 'v3nDpASs',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

###############################
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "static_live")

LOGIN_REDIRECT_URL = '/'

# VMS settings
VMS_URL = "http://vms-deone.c9users.io/vouchers/"
VOUCHER_GET_URL = VMS_URL + "get/"
VOUCHER_VALUES_URL = VMS_URL + "values/"
VOUCHER_REDEEM_URL = VMS_URL + "redeem/"
VOUCHER_STUB_INSERT_URL = VMS_URL + "insert/"
VOUCHER_STUB_DELETE_URL = VMS_URL + "delete/"
VOUCHER_DOWNLOAD_PATH = os.path.join(BASE_DIR, 'downloads')

VENDS_PER_PAGE = 15

# Billing settings
BILLING_URL = "http://billing-deone.c9users.io/"
ACCOUNT_RECHARGE_URL = BILLING_URL + "accounts/topup/"
ACCOUNT_CREATE_URL = BILLING_URL + "accounts/create_test/"

# SMS settings - SMSGH
SMS_URL = 'https://api.smsgh.com/v3/messages/send'
SMS_PARAMS = {
    'From': 'XWF',
    'ClientId': 'qtrufcsm',
    'ClientSecret': 'mgzqaxfe',
    'RegisteredDelivery': 'true'
}

TOPUP_ACCOUNT = True
VOUCHER_TYPES = ['STD']
VOUCHER_VALUES = [1, 2, 5, 10, 20]
VOUCHER_TYPES_MAP = {
    'INS': 'Instant',
    'STD': 'Standard'
}

PHONE_NUMBER_PREFIXES = ['020', '023', '024', '026', '027', '028', '050', '052', '054', '055', '056', '057']