from django.forms import ValidationError
from django.contrib.auth.models import User

from ..helpers import get_price_choices
from ..forms import VendForm

from . import Tests, VMS

class VendFormTest(Tests):
    def setUp(self):
        super(VendFormTest, self).setUp()
        self.vms = VMS()
        self.vms_user = self.vms.create_vms_user()
        self.std_voucher = self.vms.create_voucher(self.vms_user, pin='1234567891234')

    def test_clean(self):
        voucher_type = 'STD'
        prices = get_price_choices(voucher_type)

        data = {'subscriber_phone_number': '0001234567', 'voucher_value': '5.00'}
        form = VendForm(data, user=self.user, prices=prices, voucher_type=voucher_type)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'][0], 'Provide a valid phone number.')

    def tearDown(self):
        self.vms.delete_vms_user(self.vms_user)
        self.vms.delete_std_voucher(self.std_voucher)