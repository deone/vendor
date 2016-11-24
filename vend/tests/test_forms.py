from django.test import SimpleTestCase
from django.contrib.auth.models import User
from django.conf import settings

from ..helpers import get_price_choices, send_api_request
from ..forms import VendStandardVoucherForm

class VendStandardVoucherFormTest(SimpleTestCase):

    def setUp(self):
        # Create test voucher
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        self.voucher = send_api_request(settings.VOUCHER_STUB_INSERT_URL, data={'voucher_type': 'STD', 'pin': '12345678901234'})
        self.data = {'phone_number': '0542751610', 'value': '5'}
        self.prices = get_price_choices('STD')

    def test_clean_phone_number(self):
        data = {'phone_number': '0001234567', 'value': '5'}
        form = VendStandardVoucherForm(data, user=self.user, prices=self.prices)
        
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone_number'][0], 'Provide a valid phone number.')
        
        form = VendStandardVoucherForm(self.data, user=self.user, prices=self.prices)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})

    def test_save(self):
        created = send_api_request(settings.ACCOUNT_CREATE_URL, data={'username': '0542751610'})
        self.assertEqual(created['status'], 'ok')

        form = VendStandardVoucherForm(self.data, user=self.user, prices=self.prices)
        self.assertTrue(form.is_valid())

        response = form.save()
        self.assertTrue(response['recharged'])
        self.assertEqual(response['message'], 'Account recharge successful.')

    def tearDown(self):
        self.user.delete()
        # Delete test voucher
        send_api_request(settings.VOUCHER_STUB_DELETE_URL, data={'voucher_id': self.voucher['id'], 'voucher_type': 'STD'})