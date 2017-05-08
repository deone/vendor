from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vendor_test',
        'USER': 'vendor',
        'PASSWORD': 'v3nDpASs',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}

VMS_URL = 'http://154.117.12.5:8080/vouchers/'

BILLING_URL = 'http://154.117.12.4/'