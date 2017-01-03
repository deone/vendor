from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Vendor(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=10)
    company_name = models.CharField(max_length=50)
    
    def __str__(self):
        return '%s, %s' % (self.user.get_full_name(), self.company_name)
    
    def to_dict(self):
        return {
            'vendor_id': self.pk,
            'name': self.user.get_full_name(),
            'phone_number': self.phone_number,
            'company_name': self.company_name
        }

class Vend(models.Model):

    INSTANT = 'INS'
    STANDARD = 'STD'

    TYPE_CHOICES = (
        ('', 'Select Type'),
        (STANDARD, 'Standard'),
        (INSTANT, 'Instant'),
    )

    vendor = models.ForeignKey(Vendor)
    subscriber_phone_number = models.CharField(max_length=10)
    voucher_id = models.PositiveSmallIntegerField(null=True)
    voucher_value = models.DecimalField(max_digits=4, decimal_places=2)
    voucher_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    vend_date = models.DateTimeField(default=timezone.now)
    
    def occurred_today(self, now):
        return [self.vend_date.year, self.vend_date.month, self.vend_date.day] == [now.year, now.month, now.day]

    def occurred_this_week(self):
        pass
        # return (self.vend_date >= self.vend_date - 7) and (self.vend_date <= now)

    def occurred_this_month(self):
        pass

    def __str__(self):
        return "%s - %s - %s" % (self.vendor.company_name, self.subscriber_phone_number, str(self.voucher_value))