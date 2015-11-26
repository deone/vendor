from django import forms
from django.conf import settings

from vend.helpers import send_api_request

class VendForm(forms.Form):
    value = forms.ChoiceField(label='Value', choices=settings.PRICE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.ChoiceField(label='Quantity', choices=settings.QUANTITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(VendForm, self).__init__(*args, **kwargs)

    def save(self):
        url = settings.VOUCHER_FETCH_URL
        data = {'vendor_id': self.user.pk}
        data.update(self.cleaned_data)

        return send_api_request(url, data)
