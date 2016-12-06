from django import forms
from django.conf import settings
from django.utils import timezone
from django.template import loader
from django.http import HttpResponse

from utils import send_api_request, write_vouchers, file_generator, zeropad

from .models import Vend

import requests

class VendForm(forms.Form):
    phone_number = forms.CharField(label='Phone Number', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.voucher_type = kwargs.pop('voucher_type', None)
        prices = kwargs.pop('prices', None)
        super(VendForm, self).__init__(*args, **kwargs)
        self.fields['value'] = forms.ChoiceField(label='Value', choices=prices, widget=forms.Select(attrs={'class': 'form-control'}))

    def clean_phone_number(self):
        cleaned_data = super(VendForm, self).clean()
        phone_number = cleaned_data.get('phone_number')
        if phone_number[:3] not in settings.PHONE_NUMBER_PREFIXES:
            raise forms.ValidationError('Provide a valid phone number.', code='number_invalid')

        return phone_number

    def save(self):
        url = settings.VOUCHER_GET_URL
        data = {'vendor_id': self.user.vendor.pk, 'voucher_type': self.voucher_type, 'value': self.cleaned_data['value']}

        # Get voucher from VMS
        response = send_api_request(url, data)
        pin = response['results'][0][1]

        if self.voucher_type == 'STD':
            if not settings.TOPUP_ACCOUNT:
                file_name = 'Vouchers_Standard_'
            else:
                # Redeem voucher and recharge subscriber account if TOPUP_ACCOUNT is True.
                redeemed_voucher = send_api_request(settings.VOUCHER_REDEEM_URL, {'pin': pin})
                amount = redeemed_voucher['value']
                serial_no = redeemed_voucher['serial_number']

                recharge = send_api_request(settings.ACCOUNT_RECHARGE_URL, {
                    'phone_number': self.cleaned_data['phone_number'],
                    'amount': amount,
                    'serial_no': serial_no,
                })

                Vend.objects.create(
                    vendor=self.user.vendor,
                    subscriber_phone_number=self.cleaned_data['phone_number'],
                    voucher_id=serial_no,
                    voucher_value=amount,
                    voucher_type=self.voucher_type
                    )

                # Send sms notification to vendor and subscriber.
                if recharge['code'] == 200:
                    context = {
                        'serial_no': zeropad(serial_no),
                        'pin': pin,
                        'amount': amount,
                        'phone_number': self.cleaned_data['phone_number']
                    }

                    params = settings.SMS_PARAMS

                    # Send recharge notification to subscriber
                    subscriber_message = loader.render_to_string('vend/sms_subscriber.txt', context)
                    subscriber_phone_number = '+233' + self.cleaned_data['phone_number'][1:]
                    params.update({'Content': subscriber_message, 'To': subscriber_phone_number})
                    requests.get(settings.SMS_URL, params)

                    # Send recharge notification to vendor
                    vendor_message = loader.render_to_string('vend/sms_vendor.txt', context)
                    vendor_phone_number = '+233' + self.user.vendor.phone_number[1:]
                    params.update({'Content': vendor_message, 'To': vendor_phone_number})
                    requests.get(settings.SMS_URL, params)

                return recharge

        elif self.voucher_type == 'INS':
            file_name = 'Vouchers_Instant_'

        # Write vouchers to file and return download
        file_name += timezone.now().strftime('%d-%m-%Y_%I:%M') + '.txt'
        _file = settings.VOUCHER_DOWNLOAD_PATH + '/' + file_name

        f = write_vouchers(response['results'], _file)

        download = HttpResponse(file_generator(f), content_type='text/plain')
        download['Content-Disposition'] = 'attachment; filename="%s"' % file_name

        Vend.objects.create(
            vendor=self.user.vendor,
            subscriber_phone_number=self.cleaned_data['phone_number'],
            voucher_id=response['results'][0][0],
            voucher_value=self.cleaned_data['value'],
            voucher_type=self.voucher_type
            )

        return download