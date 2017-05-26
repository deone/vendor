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

# VMS settings
VMS_URL = 'http://154.117.12.5:8080/vouchers/'
VOUCHER_GET_URL = VMS_URL + 'get'
VOUCHER_INVALIDATE_URL = VMS_URL + 'invalidate'
VOUCHER_VALUES_URL = VMS_URL + 'values/'
VOUCHER_TEST_USER_CREATE_URL = VMS_URL + 'create_test_user'
VOUCHER_TEST_USER_DELETE_URL = VMS_URL + 'delete_test_user'
VOUCHER_STUB_INSERT_URL = VMS_URL + 'create_test_voucher'
VOUCHER_STUB_DELETE_URL = VMS_URL + 'delete_test_voucher'

# Billing settings
BILLING_URL = 'http://154.117.12.4/'
ACCOUNT_GET_URL = BILLING_URL + 'accounts/get'
ACCOUNT_RECHARGE_URL = BILLING_URL + 'accounts/recharge'
ACCOUNT_CREATE_URL = BILLING_URL + 'accounts/create_test_account'
ACCOUNT_DELETE_URL = BILLING_URL + 'accounts/delete_test_account'