from django import forms
from django.conf import settings

from utils import send_api_request

class Common(forms.Form):
    quantity = forms.ChoiceField(label='Quantity', choices=settings.QUANTITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        prices = kwargs.pop('prices', None)
        super(Common, self).__init__(*args, **kwargs)
        self.fields['value'] = forms.ChoiceField(label='Value', choices=prices, widget=forms.Select(attrs={'class': 'form-control'}))

class VendInstantVoucherForm(Common):

    def save(self):
        url = settings.VOUCHER_FETCH_URL
        data = {'vendor_id': self.user.pk, 'voucher_type': 'INS'}
        data.update(self.cleaned_data)

        return send_api_request(url, data)

class VendStandardVoucherForm(Common):

    def save(self):
        url = settings.VOUCHER_FETCH_URL
        data = {'vendor_id': self.user.pk, 'voucher_type': 'STD'}
        data.update(self.cleaned_data)

        return send_api_request(url, data)
