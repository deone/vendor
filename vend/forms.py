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
        # Get voucher from VMS
        # Redeem voucher and recharge customer account if TOPUP_ACCOUNT is True.
        # Send customer receipt if SEND_CUSTOMER_RECEIPT is True.
        # Send vendor receipt if SEND_VENDOR_RECEIPT is True.

        url = settings.VOUCHER_GET_URL
        data = {'vendor_id': self.user.vendor.pk, 'voucher_type': self.voucher_type, 'value': self.cleaned_data['value']}

        # Get voucher
        response = send_api_request(url, data)

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

        """ # Recharge customer account
        # Redeem voucher
        redeemed_voucher = send_api_request(settings.VOUCHER_REDEEM_URL, {'pin': pin})
        amount = redeemed_voucher['value']

        recharge = send_api_request(settings.ACCOUNT_RECHARGE_URL, {
            'phone_number': self.cleaned_data['phone_number'],
            'amount': amount,
            'serial_no': redeemed_voucher['serial_number'],
        })

        response = {}
        if recharge['code'] == 200:
            # Send recharge notification
            context = {
                'serial_no': serial_no,
                'pin': pin,
                'amount': amount,
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
        return response """