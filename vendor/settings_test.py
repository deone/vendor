from settings import *

DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['154.117.8.19']

VMS_URL = "http://154.117.8.19:8090/vouchers/"

VOUCHER_FETCH_URL = VMS_URL + "fetch/"

VOUCHER_VALUES_URL = VMS_URL + "values/"

VOUCHER_STUB_INSERT_URL = VMS_URL + "insert/"

VOUCHER_STUB_DELETE_URL = VMS_URL + "delete/"
