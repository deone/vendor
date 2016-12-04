from django.test import SimpleTestCase
from django.contrib.auth.models import User
from django.conf import settings

from ..helpers import get_price_choices, send_api_request
from ..forms import VendStandardVoucherForm

from ..models import Vendor

class VendStandardVoucherFormTest(SimpleTestCase):

    def setUp(self):
        # Create test voucher
        self.user = User.objects.create_user('a@a.com', 'a@a.com', '12345')
        Vendor.objects.create(user=self.user, company_name='Test')
        self.voucher = send_api_request(settings.VOUCHER_STUB_INSERT_URL, data={'voucher_type': 'STD', 'pin': '12345678901234'})

    def test_clean_phone_number(self):
        # Get voucher prices
        prices = get_price_choices('STD')

        data = {'phone_number': '0001234567', 'value': '5'}
        form = VendStandardVoucherForm(data, user=self.user, prices=prices)
        
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone_number'][0], 'Provide a valid phone number.')
        
        data = {'phone_number': '0543751610', 'value': '5'}
        form = VendStandardVoucherForm(data, user=self.user, prices=prices)
        
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})

    def test_save_valid_account(self):
        created = send_api_request(settings.ACCOUNT_CREATE_URL, data={'username': '0231802940'})
        self.assertEqual(created['status'], 'ok')

        # Get voucher prices
        prices = get_price_choices('STD')

        # Vend
        data = {'phone_number': '0231802940', 'value': '5'}
        form = VendStandardVoucherForm(data, user=self.user, prices=prices)

        # Test
        self.assertTrue(form.is_valid())
        response = form.save()
        self.assertTrue(response['recharged'])
        self.assertEqual(response['message'], 'Account recharge successful.')
        
    def test_save_account_not_exist(self):
        # Get voucher prices
        prices = get_price_choices('STD')

        # Vend
        data = {'phone_number': '0544433333', 'value': '5'}
        form = VendStandardVoucherForm(data, user=self.user, prices=prices)

        # Test
        self.assertTrue(form.is_valid())
        response = form.save()
        self.assertFalse(response['recharged'])
        self.assertEqual(response['message'], 'Account does not exist.')

    def tearDown(self):
        self.user.delete()
        # Delete test voucher
        send_api_request(settings.VOUCHER_STUB_DELETE_URL, data={'voucher_id': self.voucher['id'], 'voucher_type': 'STD'})