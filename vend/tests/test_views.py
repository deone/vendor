from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings

from ..forms import VendStandardVoucherForm, VendInstantVoucherForm
from ..models import Vendor
from ..views import index
from ..helpers import send_api_request, get_price_choices

class ViewsTests(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('z@z.com', 'z@z.com', '12345')

    def test_index_get(self):
        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})
        response = self.c.get(reverse('vend_instant'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response, 'vend/vend_instant.html')
        self.assertTrue(isinstance(response.context['form'], VendInstantVoucherForm))

    def test_index_post(self):
        self.c.post(reverse('login'), {'username': 'z@z.com', 'password': '12345'})

        factory = RequestFactory()
        session = SessionMiddleware()

        pin_one = {'pin': '12345678901234'}
        pin_two = {'pin': '12345678901233'}

        send_api_request(settings.VOUCHER_STUB_INSERT_URL, pin_one)
        send_api_request(settings.VOUCHER_STUB_INSERT_URL, pin_two)

        prices = get_price_choices('STD')

        vendor = Vendor.objects.create(user=self.user, company_name="Vender Inc.")
        request = factory.post(reverse('vend_standard'), data={'value': 5, 'quantity': 2})
        request.user = self.user

        response = index(request, template='vend/vend_standard.html', vend_form=VendStandardVoucherForm, prices=prices)

        send_api_request(settings.VOUCHER_STUB_DELETE_URL, pin_one)
        send_api_request(settings.VOUCHER_STUB_DELETE_URL, pin_two)

        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertNotEqual(response.content, '')
