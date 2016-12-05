from django import forms
from django.conf import settings

from utils import send_api_request

class VendForm(forms.Form):
    phone_number = forms.CharField(label='Phone Number', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        prices = kwargs.pop('prices', None)
        super(VendForm, self).__init__(*args, **kwargs)
        self.fields['value'] = forms.ChoiceField(label='Value', choices=prices, widget=forms.Select(attrs={'class': 'form-control'}))

    def clean_phone_number(self):
        cleaned_data = super(VendForm, self).clean()
        phone_number = cleaned_data.get('phone_number')
        if phone_number[:3] not in settings.PHONE_NUMBER_PREFIXES:
            raise forms.ValidationError('Provide a valid phone number.', code='number_invalid')