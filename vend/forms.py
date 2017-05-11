from django import forms
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from utils import send_api_request, file_generator, write_vouchers

from .models import Vend

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

    def clean(self):
        # Get (valid) voucher.
        # If voucher is standard, do these:
        # - Check whether account exists. If it doesn't, display message and exit.
        # - If it does, recharge it.
        # - If recharge succeeds, invalidate voucher.

        cleaned_data = super(VendForm, self).clean()

        # Get voucher
        voucher = self.get_info_or_display_error(settings.VOUCHER_GET_URL, {
            'voucher_type': self.voucher_type, 'value': self.cleaned_data['value']
        })

        if self.voucher_type == 'STD':
            # Get account
            account = self.get_info_or_display_error(settings.ACCOUNT_GET_URL, {
                'phone_number': cleaned_data.get('phone_number')
            })

            # Recharge account
            recharge = self.get_info_or_display_error(settings.ACCOUNT_RECHARGE_URL, {
                'username': account['username'],
                'amount': cleaned_data.get('value'),
                'serial_no': voucher['serial_no']
            })

            # Invalidate voucher
            response = self.get_info_or_display_error(settings.VOUCHER_INVALIDATE_URL, {
                'voucher_id': voucher['serial_no'],
                'vendor_id': self.user.vendor.pk
            })

        cleaned_data.update({'voucher': voucher})

    def get_info_or_display_error(self, url, data):
        r = send_api_request(url, data)
        json = r.json()

        if r.status_code != 200:
            raise forms.ValidationError(_(json['message']), code=_(json['code']))

        return json

    def save(self):
        voucher = self.cleaned_data['voucher']

        # Create vend entry
        Vend.objects.create(
            vendor=self.user.vendor,
            subscriber_phone_number=self.cleaned_data['phone_number'],
            voucher_id=voucher['serial_no'],
            voucher_value=self.cleaned_data['value'],
            voucher_type=self.voucher_type
        )

        if self.voucher_type == 'INS':
            # Download voucher if voucher type is instant
            file_name = 'Vouchers_Instant_'

            # Write vouchers to file and return download
            file_name += timezone.now().strftime('%d-%m-%Y_%I:%M') + '.txt'
            _file = settings.VOUCHER_DOWNLOAD_PATH + '/' + file_name

            f = write_vouchers([voucher], _file)
            download = HttpResponse(file_generator(f), content_type='text/plain')
            download['Content-Disposition'] = 'attachment; filename="%s"' % file_name

            return download
        else:
            # Send receipts - use signals on Vend model.
            # Return voucher
            return self.cleaned_data['voucher']

        """ # Get voucher from VMS
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

                # Create vend entry and send sms notification to vendor and subscriber if topup was successful.
                if recharge['code'] == 200:
                    Vend.objects.create(
                        vendor=self.user.vendor,
                        subscriber_phone_number=self.cleaned_data['phone_number'],
                        voucher_id=serial_no,
                        voucher_value=amount,
                        voucher_type=self.voucher_type
                        )

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
                    # requests.get(settings.SMS_URL, params)

                    # Send recharge notification to vendor
                    vendor_message = loader.render_to_string('vend/sms_vendor.txt', context)
                    vendor_phone_number = '+233' + self.user.vendor.phone_number[1:]
                    params.update({'Content': vendor_message, 'To': vendor_phone_number})
                    # requests.get(settings.SMS_URL, params)

                return recharge """