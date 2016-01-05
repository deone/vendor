from settings import *

DEBUG = TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['154.117.8.18']

STATIC_URL = "/static/"

VMS_URL = "http://154.117.8.18:8090/vouchers/"

VOUCHER_FETCH_URL = VMS_URL + "fetch/"

VOUCHER_VALUES_URL = VMS_URL + "values/"

VOUCHER_STUB_INSERT_URL = VMS_URL + "insert/"

VOUCHER_STUB_DELETE_URL = VMS_URL + "delete/"
