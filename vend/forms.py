from django import forms
from django.conf import settings

from vend.helpers import send_api_request

import requests

def get_price_choices():
    lst = [('', 'Select Price')]
    prices = requests.get(settings.VOUCHER_VALUES_URL)
    for p in prices.json()['results']:
        lst.append((p, str(p) + ' GHS'))
    return lst

class VendForm(forms.Form):
    value = forms.ChoiceField(label='Value', choices=get_price_choices(), widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.ChoiceField(label='Quantity', choices=settings.QUANTITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(VendForm, self).__init__(*args, **kwargs)

    def save(self):
        url = settings.VOUCHER_FETCH_URL
        data = {'vendor_id': self.user.pk}
        data.update(self.cleaned_data)

        return send_api_request(url, data)
