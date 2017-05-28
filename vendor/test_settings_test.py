from django.test import SimpleTestCase

from settings_test import *

class TestSettingsTest(SimpleTestCase):
    def test_settings(self):
        self.assertEqual(DATABASES['default']['NAME'], 'vendor_test')
        self.assertEqual(VMS_URL, 'http://154.117.12.5:8080/vouchers/')
        self.assertEqual(BILLING_URL, 'http://154.117.12.4/')