from settings import *

DEBUG = False

# VMS settings
VMS_URL = 'http://154.117.12.5/vouchers/'
VOUCHER_GET_URL = VMS_URL + 'get'
VOUCHER_INVALIDATE_URL = VMS_URL + 'invalidate'
VOUCHER_VALUES_URL = VMS_URL + 'values/'
VOUCHER_STUB_INSERT_URL = VMS_URL + 'insert/'
VOUCHER_STUB_DELETE_URL = VMS_URL + 'delete/'

# Billing settings
BILLING_URL = 'http://xwf.spectrawireless.com/'
ACCOUNT_GET_URL = BILLING_URL + 'accounts/get'
ACCOUNT_RECHARGE_URL = BILLING_URL + 'accounts/recharge'
ACCOUNT_CREATE_URL = BILLING_URL + 'accounts/create_test/'