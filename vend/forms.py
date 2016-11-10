from django import forms
from django.conf import settings
from django.template import loader

from twilio.rest import TwilioRestClient

from .helpers import send_api_request

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

class VendStandardVoucherForm(forms.Form):
    phone_number = forms.CharField(label='Phone Number', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        prices = kwargs.pop('prices', None)
        super(VendStandardVoucherForm, self).__init__(*args, **kwargs)
        self.fields['value'] = forms.ChoiceField(label='Value', choices=prices, widget=forms.Select(attrs={'class': 'form-control'}))
        
    def clean_phone_number(self):
        cleaned_data = super(VendStandardVoucherForm, self).clean()
        phone_number = cleaned_data.get('phone_number')
        if phone_number[:3] not in settings.PHONE_NUMBER_PREFIXES:
            raise forms.ValidationError('Provide a valid phone number.', code='number_invalid')

    def save(self):
        url = settings.VOUCHER_FETCH_URL
        data = {'vendor_id': self.user.pk, 'voucher_type': 'STD'}
        data.update(self.cleaned_data)
        data.update({'quantity': settings.VEND_QUANTITY})

        # Get voucher
        response = send_api_request(url, data)
        
        # Send verification sms
        context = {
            'serial_no': response['results'][0][0],
            'pin': response['results'][0][1],
        }
        
        message = loader.render_to_string('vend/sms.txt', context)
        
        phone_number = '+233' + self.cleaned_data['phone_number'][1:]
        client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(to=phone_number, from_=settings.TWILIO_NUMBER, body=message)