from settings import *

DEBUG = TEMPLATE_DEBUG = True

IP = '154.117.8.19'

ALLOWED_HOSTS = [IP]

VMS_URL = "http://" + IP + ":8090/vouchers/"

VOUCHER_FETCH_URL = VMS_URL + "fetch/"

VOUCHER_VALUES_URL = VMS_URL + "values/"

VOUCHER_STUB_INSERT_URL = VMS_URL + "insert/"

VOUCHER_STUB_DELETE_URL = VMS_URL + "delete/"
