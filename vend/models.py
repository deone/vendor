from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
    subscriber_phone_number = models.CharField(max_length=10, null=True)
    voucher_id = models.PositiveSmallIntegerField(null=True)
    voucher_value = models.DecimalField(max_digits=4, decimal_places=2)
    voucher_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    vend_date = models.DateTimeField(default=timezone.now)

    def occurred(self, **kwargs):
        year = kwargs.get('year', None)
        month = kwargs.get('month', None)
        day = kwargs.get('day', None)

        if year and month and day:
            return [self.vend_date.year, self.vend_date.month, self.vend_date.day] == [year, month, day]
        elif year and month and day is None:
            return [self.vend_date.year, self.vend_date.month] == [year, month]
        elif year and month is None and day is None:
            return self.vend_date.year == year

    def occurred_between(self, start, end):
        return start <= self.vend_date.date() <= end

    def __str__(self):
        return "%s - %s - %s" % (self.vendor.company_name, self.subscriber_phone_number, str(self.voucher_value))