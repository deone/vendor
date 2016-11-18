from settings import *

DEBUG = False

IP = '154.117.8.18'
ALLOWED_HOSTS = [IP]

VMS_URL = "http://" + IP + ":8090/vouchers/"
VOUCHER_FETCH_URL = VMS_URL + "fetch/"
VOUCHER_VALUES_URL = VMS_URL + "values/"
VOUCHER_STUB_INSERT_URL = VMS_URL + "insert/"
VOUCHER_STUB_DELETE_URL = VMS_URL + "delete/"
VOUCHER_REDEEM_URL = VMS_URL + "redeem/"

# Billing settings
ACCOUNT_RECHARGE_URL = "http://xwf.spectrawireless.com/accounts/topup/"