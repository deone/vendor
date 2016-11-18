from django import forms
from django.conf import settings
from django.template import loader

import requests

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

        return phone_number

    def save(self):
        url = settings.VOUCHER_FETCH_URL
        data = {'vendor_id': self.user.pk, 'voucher_type': 'STD'}
        data.update(self.cleaned_data)
        data.update({'quantity': settings.VEND_QUANTITY})

        # Get voucher
        voucher = send_api_request(url, data)
        serial_no = voucher['results'][0][0]
        pin = voucher['results'][0][1]
        
        # Redeem voucher
        redeemed_voucher = send_api_request(settings.VOUCHER_REDEEM_URL, {'pin': pin})

        # Recharge customer account
        recharge = send_api_request(settings.ACCOUNT_RECHARGE_URL, {
            'phone_number': self.cleaned_data['phone_number'],
            'amount': redeemed_voucher['value'],
            'serial_no': redeemed_voucher['serial_number'],
        })
        
        response = {}
        if recharge['code'] == 200:
            # Send recharge notification
            context = {
                'serial_no': serial_no,
                'pin': pin,
            }

            message = loader.render_to_string('vend/sms.txt', context)

            params = settings.SMS_PARAMS
            phone_number = '+233' + self.cleaned_data['phone_number'][1:]
            params.update({'Content': message, 'To': phone_number})
            sms_response = requests.get(settings.SMS_URL, params)

            response.update({'recharged': True})
        else:
            response.update({'recharged': False})

        response.update({'message': recharge['message']})
        return response