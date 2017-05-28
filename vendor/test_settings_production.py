from django.test import SimpleTestCase

from settings_production import *

class TestSettingsProduction(SimpleTestCase):
    def test_settings(self):
        self.assertFalse(DEBUG)
        self.assertEqual(VMS_URL, 'http://154.117.12.5/vouchers/')
        self.assertEqual(BILLING_URL, 'http://xwf.spectrawireless.com/')