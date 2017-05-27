from django.test import SimpleTestCase, TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse

from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages import get_messages
from django.conf import settings

from ..forms import VendForm
from ..models import Vend
from ..views import STDVendView, INSVendView
from utils import send_api_request, get_price_choices

from . import Tests, VMS, create_vend

from datetime import datetime

class VendViewTests(Tests):
    def setUp(self):
        self.c = Client()
        super(VendViewTests, self).setUp()
        self.c.post('/login', {'username': 'p@p.com', 'password': '12345'})
    
class VendViewGETTests(VendViewTests):
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

class VendViewPOSTTests(VendViewTests):
    def setUp(self):
        super(VendViewPOSTTests, self).setUp()
        self.factory = RequestFactory()
        self.account = send_api_request(settings.ACCOUNT_CREATE_URL, {
            'username': '0231802941',
            'password': '12345'
        }).json()

        self.vms = VMS()
        self.vms_user = self.vms.create_user()
        self.std_voucher = self.vms.create_voucher(self.vms_user, pin='1234567891234')

    def _process_request(self, request):
        request.user = self.user
        session = SessionMiddleware()
        session.process_request(request)
        request.session.save()
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def _message_list(self, request):
        storage = get_messages(request)
        lst = []
        for message in storage:
            lst.append(message)
        return lst

    def _today(self):
        today = datetime.today()
        return {
            'year': str(today.year),
            'month': str(today.month),
            'day': str(today.day)
        }

    def _check_response(self, response):
        self.assertTrue('vendors' in response)
        self.assertTrue({'count': 1, 'value': 5} in response['vendors'][0]['vend_count'])
        self.assertTrue('voucher_values' in response)

    def _build_query_string(self, **kwargs):
        string = '/vends?'
        for item in kwargs.iteritems():
            item = list(item)
            if item[0] == 'from_':
                item[0] = 'from'
            string += ('%s%s%s%s') % (item[0], '=', item[1], '&')
        return string[:-1]

    def test_post(self):
        request = self.factory.post('/', {'subscriber_phone_number': self.account['username'], 'voucher_value': '5.0'})
        self._process_request(request)

        response = STDVendView.as_view()(request)

        lst = self._message_list(request)

        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('Vend successful.', lst[0].__str__())
        self.assertEqual(response.get('location'), '/')

    def test_post_instant_voucher(self):
        voucher = self.vms.create_voucher(self.vms_user, voucher_type='INS', username='a@a.com', password='12345')
        request = self.factory.post('/vend/instant', {'subscriber_phone_number': '', 'voucher_value': '5.0'})
        self._process_request(request)

        response = INSVendView.as_view()(request)
        self.assertEqual(response['Content-Type'], 'text/plain')

        self.vms.delete_voucher(voucher['id'], 'INS')

    def test_get_user_vends(self):
        create_vend(self.user.vendor, self.std_voucher)

        response = self.c.get('/my_vends')
        self.assertTrue('vends' in response.context)

    def test_get_user_vends_no_vends(self):
        response = self.c.get('/my_vends')
        self.assertEqual(response.context['message'], 'No vends found.')

    def test_get_vendor_vend_count_year(self):
        create_vend(self.user.vendor, self.std_voucher)
        query_string = self._build_query_string(year=self._today()['year'])

        response = self.c.get(query_string).json()
        self._check_response(response)

    def test_get_vendor_vend_count_year_month(self):
        create_vend(self.user.vendor, self.std_voucher)
        query_string = self._build_query_string(year=self._today()['year'], month=self._today()['month'])

        response = self.c.get(query_string).json()
        self._check_response(response)

    def test_get_vendor_vend_count_year_month_day(self):
        create_vend(self.user.vendor, self.std_voucher)
        query_string = self._build_query_string(year=self._today()['year'], month=self._today()['month'], day=self._today()['day'])

        response = self.c.get(query_string).json()
        self._check_response(response)

    def test_get_vendor_vend_count_from_to(self):
        create_vend(self.user.vendor, self.std_voucher)
        date = '%(day)s-%(month)s-%(year)s' % self._today()
        query_string = self._build_query_string(from_=date, to=date)

        response = self.c.get(query_string).json()
        self._check_response(response)

    def tearDown(self):
        send_api_request(settings.ACCOUNT_DELETE_URL, {
            'username': self.account['username']
        })
        self.vms.delete_user(self.vms_user)
        self.vms.delete_voucher(self.std_voucher['id'], 'STD')