from django import forms
from django.conf import settings

from .helpers import send_api_request

import requests

def get_price_choices():
    lst = [('', 'Select Price')]
    prices = requests.get(settings.VOUCHER_VALUES_URL).json()
    for p in prices['results']:
        lst.append((p, str(p) + ' GHS'))
    return lst

class Common(forms.Form):
    value = forms.ChoiceField(label='Value', choices=get_price_choices(), widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.ChoiceField(label='Quantity', choices=settings.QUANTITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(Common, self).__init__(*args, **kwargs)

class VendInstantVoucherForm(Common):
    pass

class VendStandardVoucherForm(Common):

    def save(self):
        print self.cleaned_data
        url = settings.VOUCHER_FETCH_URL
        data = {'vendor_id': self.user.pk, 'voucher_type': 'STD'}
        data.update(self.cleaned_data)

        return send_api_request(url, data)
