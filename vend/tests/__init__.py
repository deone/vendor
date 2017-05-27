from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from utils import send_api_request
from ..models import Vendor, Vend

class VMS(object):
    def create_user(self):
        return send_api_request(settings.VOUCHER_TEST_USER_CREATE_URL, {
            'username': 'z@z.com'
        }).json()

    def delete_user(self, user):
        return send_api_request(settings.VOUCHER_TEST_USER_DELETE_URL, {
            'username': user['username']
        }).json()

    def create_voucher(self, vms_user, voucher_type='STD', pin=None, username=None, password=None):
        dct = {
            'voucher_type': voucher_type,
            'creator': vms_user['username'],
        }

        if voucher_type == 'STD':
            dct.update({'pin': pin})
        else:
            dct.update({'username': username, 'password': password})

        return send_api_request(settings.VOUCHER_STUB_INSERT_URL, dct).json()

    def delete_voucher(self, voucher_id, voucher_type):
        return send_api_request(settings.VOUCHER_STUB_DELETE_URL, {
            'voucher_id': voucher_id,
            'voucher_type': voucher_type
        }).json()

def create_user():
    user = User.objects.create_user('p@p.com', 'p@p.com', '12345')
    user.first_name = 'Dayo'
    user.last_name = 'Osikoya'
    return user

def create_vendor(user):
    return Vendor.objects.create(user=user, phone_number='0543221234', company_name='Test Co.', voucher_type='STD')

def create_vend(vendor, voucher):
    return Vend.objects.create(
        vendor=vendor,
        subscriber_phone_number='0231802940',
        voucher_id=voucher['id'],
        voucher_value=5,
        voucher_type='STD'
    )

class Tests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.vendor = create_vendor(self.user)

    def tearDown(self):
        self.user.delete()