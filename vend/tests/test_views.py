from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages
from django.conf import settings

from ..forms import VendForm
from ..models import Vendor
from ..views import VendView
from ..helpers import send_api_request, get_price_choices

class VendViewTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user('p@p.com', 'p@p.com', '12345')
        self.vendor = Vendor.objects.create(user=self.user, phone_number='0543221234', company_name='Test Co.', voucher_type='STD')
        self.vms_user = send_api_request(settings.VOUCHER_TEST_USER_CREATE_URL, {
            'username': 'z@z.com'
        })

        self.std_voucher = send_api_request(settings.VOUCHER_STUB_INSERT_URL, {
            'pin': '12345678901234',
            'voucher_type': 'STD',
            'creator': self.vms_user['username'],
            'quantity': 10,
            'value': 5
        })

        self.c.post('/login', {'username': 'p@p.com', 'password': '12345'})

    def test_get(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response, 'vend/vend_standard.html')
        self.assertTrue(isinstance(response.context['form'], VendForm))

    def test_get_instant_voucher(self):
        self.vendor.voucher_type = 'INS'
        self.vendor.save()

        response = self.c.get('/vend/instant')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response, 'vend/vend_instant.html')
        self.assertTrue(isinstance(response.context['form'], VendForm))

        response = self.c.get('/')
        self.assertEqual(response.status_code, 302)

    def process_request(self, request):
        request.user = self.user
        session = SessionMiddleware()
        session.process_request(request)
        request.session.save()
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def message_list(self, request):
        storage = get_messages(request)
        lst = []
        for message in storage:
            lst.append(message)
        return lst

    def check_response(self, response, message, msg_list):
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(message, msg_list[0].__str__())
        self.assertEqual(response.get('location'), '/')

    def test_post(self):
        request = self.factory.post('/', {'subscriber_phone_number': '0231802940', 'voucher_value': '5.00'})
        self.process_request(request)

        response = VendView.as_view()(request)
        lst = self.message_list(request)
        self.check_response(response, 'Vend successful.', lst)

    def tearDown(self):
        send_api_request(settings.VOUCHER_TEST_USER_DELETE_URL, {
            'username': self.vms_user['username']
        })

        send_api_request(settings.VOUCHER_STUB_DELETE_URL, {
            'voucher_id': self.std_voucher['id'],
            'voucher_type': 'STD'
        })