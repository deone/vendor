from django.conf import settings
from django.template import loader
from django.dispatch import receiver
from django.db.models.signals import post_save

from ..models import Vend, Vendor
from utils import zeropad

import requests

@receiver(post_save, sender=Vend)
def send_receipts(sender, **kwargs):
    instance = kwargs['instance']
    context = {
        'serial_no': zeropad(instance.voucher_id),
        'amount': instance.voucher_value,
        'phone_number': instance.subscriber_phone_number
    }

    params = settings.SMS_PARAMS

    # Send recharge notification to subscriber
    subscriber_message = loader.render_to_string('vend/sms_subscriber.txt', context)
    subscriber_phone_number = '+233' + instance.subscriber_phone_number[1:]
    params.update({'Content': subscriber_message, 'To': subscriber_phone_number})
    requests.get(settings.SMS_URL, params)

    # Send recharge notification to vendor
    vendor_message = loader.render_to_string('vend/sms_vendor.txt', context)
    vendor_phone_number = '+233' + instance.vendor.phone_number[1:]
    params.update({'Content': vendor_message, 'To': vendor_phone_number})
    requests.get(settings.SMS_URL, params)