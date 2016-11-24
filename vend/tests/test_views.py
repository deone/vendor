from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages
from django.conf import settings

from ..forms import VendStandardVoucherForm
from ..models import Vendor
from ..views import index
from ..helpers import send_api_request, get_price_choices

class ViewsTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('z@z.com', 'z@z.com', '12345')
        self.voucher_one = send_api_request(settings.VOUCHER_STUB_INSERT_URL, {'pin': '12345678901234', 'voucher_type': 'STD'})
        self.voucher_two = send_api_request(settings.VOUCHER_STUB_INSERT_URL, {'pin': '12345678901233', 'voucher_type': 'STD'})

    def test_index_get(self):
        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('vend_standard'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response, 'vend/vend_standard.html')
        self.assertTrue(isinstance(response.context['form'], VendStandardVoucherForm))

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
        self.assertEqual(response.get('location'), reverse('vend_standard'))

    def test_index_post(self):
        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})

        factory = RequestFactory()
        vendor = Vendor.objects.create(user=self.user, company_name="Vender Inc.")
        prices = get_price_choices('STD')

        # Success
        request = factory.post(reverse('vend_standard'), data={'value': 5, 'phone_number': '0231802940'})
        self.process_request(request)

        response = index(request, template='vend/vend_standard.html', vend_form=VendStandardVoucherForm, prices=prices)
        lst = self.message_list(request)

        self.check_response(response, 'Account recharge successful.', lst)

        # Failure
        request = factory.post(reverse('vend_standard'), data={'value': 5, 'phone_number': '0234445555'})
        self.process_request(request)

        response = index(request, template='vend/vend_standard.html', vend_form=VendStandardVoucherForm, prices=prices)
        lst = self.message_list(request)

        self.check_response(response, 'Account does not exist.', lst)

    def tearDown(self):
        send_api_request(settings.VOUCHER_STUB_DELETE_URL, data={'voucher_id': self.voucher_one['id'], 'voucher_type': 'STD'})
        send_api_request(settings.VOUCHER_STUB_DELETE_URL, data={'voucher_id': self.voucher_two['id'], 'voucher_type': 'STD'})