from django.test import SimpleTestCase
from django.conf import settings

from utils import write_vouchers

class UtilsTests(SimpleTestCase):

    def test_write_vouchers(self):
        vouchers = [['0000000375', 'aaa@a.com', '12345'], ['0000000376', 'bbb@a.com', '12345']]
        _file = settings.VOUCHER_DOWNLOAD_PATH + '/test.csv'
        f = write_vouchers(vouchers, _file)

        self.assertTrue(f.name.endswith('.csv'))