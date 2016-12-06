from django import forms
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse

from utils import send_api_request, write_vouchers, file_generator

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

        # Redeem voucher and recharge subscriber account if TOPUP_ACCOUNT is True.
        if settings.TOPUP_ACCOUNT and self.voucher_type == 'STD':
            redeemed_voucher = send_api_request(settings.VOUCHER_REDEEM_URL, {'pin': pin})
            amount = redeemed_voucher['value']

            recharge = send_api_request(settings.ACCOUNT_RECHARGE_URL, {
                'phone_number': self.cleaned_data['phone_number'],
                'amount': amount,
                'serial_no': redeemed_voucher['serial_number'],
            })

            """ # Send sms notification to vendor and subscriber.
            if recharge['code'] == 200:
                context = {
                    'serial_no': serial_no,
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

            # Log vend. """

            return recharge

        # Write vouchers to file and return download
        if self.voucher_type == 'STD':
            file_name = 'Vouchers_Standard_'
        elif self.voucher_type == 'INS':
            file_name = 'Vouchers_Instant_'

        file_name += timezone.now().strftime('%d-%m-%Y_%I:%M') + '.txt'
        _file = settings.VOUCHER_DOWNLOAD_PATH + '/' + file_name

        f = write_vouchers(response['results'], _file)

        response = HttpResponse(file_generator(f), content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        return response