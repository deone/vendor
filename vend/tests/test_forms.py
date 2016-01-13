from django.test import SimpleTestCase
from django.contrib.auth.models import User
from django.conf import settings

from ..helpers import get_price_choices, send_api_request
from ..forms import VendInstantVoucherForm

class VendInstantVoucherFormTest(SimpleTestCase):

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
          data={'voucher_id': self.voucher['id'], 'voucher_type': 'INS'})
