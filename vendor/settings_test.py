from settings import *

IP = '154.117.8.19'
ALLOWED_HOSTS = [IP]

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

# VMS settings
VMS_URL = "http://" + IP + ":8090/vouchers/"
VOUCHER_GET_URL = VMS_URL + "get/"
VOUCHER_VALUES_URL = VMS_URL + "values/"
VOUCHER_REDEEM_URL = VMS_URL + "redeem/"
VOUCHER_STUB_INSERT_URL = VMS_URL + "insert/"
VOUCHER_STUB_DELETE_URL = VMS_URL + "delete/"

# Billing settings
BILLING_URL = "http://" + IP + "/"
ACCOUNT_RECHARGE_URL = BILLING_URL + "accounts/topup/"
ACCOUNT_CREATE_URL = BILLING_URL + "accounts/create_test/"
