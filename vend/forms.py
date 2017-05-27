from django import forms
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from utils import send_api_request, file_generator, write_vouchers

from .models import Vend

import requests

class VendForm(forms.ModelForm):
    class Meta:
        model = Vend
        fields = ['voucher_value', 'subscriber_phone_number']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.vendor = user.vendor
        self.voucher_type = kwargs.pop('voucher_type', None)
        prices = kwargs.pop('prices', None)

        super(VendForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['voucher_value'] = forms.ChoiceField(label=_('Value'),
            choices=prices, widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['subscriber_phone_number'] = forms.CharField(label=_('Phone Number'),
            max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['subscriber_phone_number'].required = False

    def clean(self):
        # Get (valid) voucher.
        # If voucher is standard, do these:
        # - Check whether account exists. If it doesn't, display message and exit.
        # - If it does, recharge it.
        # - If recharge succeeds, invalidate voucher.

        cleaned_data = super(VendForm, self).clean()

        # Get voucher
        voucher = self.get_info_or_display_error(settings.VOUCHER_GET_URL, {
            'voucher_type': self.voucher_type,
            'value': cleaned_data.get('voucher_value')
        })

        if self.voucher_type == 'STD':
            phone_number = cleaned_data.get('subscriber_phone_number')
            if phone_number[:3] not in settings.PHONE_NUMBER_PREFIXES:
                raise forms.ValidationError('Provide a valid phone number.', code='number_invalid')

            # Get account
            account = self.get_info_or_display_error(settings.ACCOUNT_GET_URL, {
                'phone_number': cleaned_data.get('subscriber_phone_number')
            })
    
            # Recharge account
            recharge = self.get_info_or_display_error(settings.ACCOUNT_RECHARGE_URL, {
                'username': account['username'],
                'amount': cleaned_data.get('voucher_value'),
                'serial_no': voucher['serial_no']
            })

        # Invalidate voucher
        response = self.get_data_or_display_error(settings.VOUCHER_INVALIDATE_URL, {
            'voucher_id': voucher['serial_no'],
            'vendor_id': self.vendor.pk,
            'voucher_type': self.voucher_type
        })

        cleaned_data.update({'voucher': voucher})

    def get_data_or_display_error(self, url, data):
        r = requests.post(url, data=data)
        json = r.json()

        if r.status_code != 200:
            raise forms.ValidationError(_(json['message']), code=_(json['code']))

        return json

    def get_info_or_display_error(self, url, data):
        r = send_api_request(url, data)
        json = r.json()

        if r.status_code != 200:
            raise forms.ValidationError(_(json['message']), code=_(json['code']))

        return json

    def save(self, commit=True):
        voucher = self.cleaned_data['voucher']
        self.instance.voucher_id = voucher['serial_no']
        self.instance.vendor = self.vendor
        self.instance.voucher_type = self.voucher_type
        vend = super(VendForm, self).save(commit)

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