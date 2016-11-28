from settings import *

IP = '154.117.8.19'
ALLOWED_HOSTS = [IP]

# VMS settings
VMS_URL = "http://" + IP + ":8090/vouchers/"
VOUCHER_FETCH_URL = VMS_URL + "fetch/"
VOUCHER_VALUES_URL = VMS_URL + "values/"
VOUCHER_STUB_INSERT_URL = VMS_URL + "insert/"
VOUCHER_STUB_DELETE_URL = VMS_URL + "delete/"
VOUCHER_REDEEM_URL = VMS_URL + "redeem/"
VEND_FETCH_URL = VMS_URL + "vends/"

# Billing settings
ACCOUNT_RECHARGE_URL = "http://" + IP + ":7700/accounts/topup/"
ACCOUNT_CREATE_URL = "http://" + IP + ":7700/accounts/create_test/"