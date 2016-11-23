from django.test import SimpleTestCase
from django.contrib.auth.models import User
from django.conf import settings

from ..helpers import get_price_choices, send_api_request
from ..forms import VendStandardVoucherForm
# from ..forms import VendInstantVoucherForm

class VendStandardVoucherFormTest(SimpleTestCase):

    def setUp(self):
        # Create test voucher
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        self.prices = get_price_choices('STD')
        self.voucher = send_api_request(settings.VOUCHER_STUB_INSERT_URL, data={'voucher_type': 'STD', 'pin': '12345678901234'})

    def test_clean_phone_number(self):
        data = {'phone_number': '0001234567', 'value': '5'}
        form = VendStandardVoucherForm(data, user=self.user, prices=self.prices)
        
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone_number'][0], 'Provide a valid phone number.')
        
        data.update({'phone_number': '0542751610'})
        form = VendStandardVoucherForm(data, user=self.user, prices=self.prices)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})

    def tearDown(self):
        # Delete test voucher
        send_api_request(settings.VOUCHER_STUB_DELETE_URL, data={'voucher_id': self.voucher['id'], 'voucher_type': 'STD'})

""" class VendInstantVoucherFormTest(SimpleTestCase):

    def setUp(self):
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        # Create voucher
        self.voucher = send_api_request(settings.VOUCHER_STUB_INSERT_URL,
            data={'username': 'a@a.com', 'password': '12345', 'voucher_type': 'INS'})

    def test_save(self):
        prices = get_price_choices('INS')
        data = {'quantity': 1, 'value': 5}
        form = VendInstantVoucherForm(data, user=self.user, prices=prices)
        form.is_valid()
        response = form.save()

        self.assertEqual(response['code'], 200)

    def tearDown(self):
        # Delete voucher
        send_api_request(settings.VOUCHER_STUB_DELETE_URL,
          data={'voucher_id': self.voucher['id'], 'voucher_type': 'INS'}) """
