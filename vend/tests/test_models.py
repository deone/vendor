from . import *

class ModelTests(Tests):
    def setUp(self):
        super(ModelTests, self).setUp()

    def test_vendor_instance(self):
        self.assertEqual(self.vendor.__str__(), 'Dayo Osikoya, Test Co.')

    def test_vend_instance(self):
        vms = VMS()

        vms_user = vms.create_user()
        voucher = vms.create_voucher(vms_user, voucher_type='STD', pin='12345678901235')

        vend = create_vend(self.user.vendor, voucher)
        self.assertEqual(vend.__str__(), 'Test Co. - 0231802940 - 5')

        vms.delete_voucher(voucher['id'], 'STD')
        vms.delete_user(vms_user)