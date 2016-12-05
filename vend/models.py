from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Vendor(models.Model):
    user = models.OneToOneField(User)
    company_name = models.CharField(max_length=50)

class Vend(models.Model):

    INSTANT = 'INS'
    STANDARD = 'STD'

    TYPE_CHOICES = (
        ('', 'Select Type'),
        (STANDARD, 'Standard'),
        (INSTANT, 'Instant'),
    )

    vendor = models.ForeignKey(Vendor)
    phone_number = models.CharField(max_length=10)
    voucher_id = models.PositiveSmallIntegerField(null=True)
    voucher_value = models.PositiveSmallIntegerField()
    voucher_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    vend_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return "%s - %s - %s" % (self.vendor.company_name, self.phone_number, str(self.value))