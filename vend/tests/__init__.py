from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from ..helpers import send_api_request
from ..models import Vendor

class VMS(object):
    def create_vms_user(self):
        return send_api_request(settings.VOUCHER_TEST_USER_CREATE_URL, {
            'username': 'z@z.com'
        })
    
    def create_std_voucher(self, vms_user):
        return send_api_request(settings.VOUCHER_STUB_INSERT_URL, {
            'pin': '12345678901234',
            'voucher_type': 'STD',
            'creator': vms_user['username'],
        })

    def delete_vms_user(self, vms_user):
        return send_api_request(settings.VOUCHER_TEST_USER_DELETE_URL, {
            'username': vms_user['username']
        })

    def delete_std_voucher(self, voucher):
        return send_api_request(settings.VOUCHER_STUB_DELETE_URL, {
            'voucher_id': voucher['id'],
            'voucher_type': 'STD'
        })

class Tests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('p@p.com', 'p@p.com', '12345')
        self.vendor = Vendor.objects.create(user=self.user, phone_number='0543221234', company_name='Test Co.', voucher_type='STD')