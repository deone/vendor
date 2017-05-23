from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Vendor

class Tests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('p@p.com', 'p@p.com', '12345')
        self.vendor = Vendor.objects.create(user=self.user, phone_number='0543221234', company_name='Test Co.', voucher_type='STD')