from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Vendor(models.Model):
    user = models.OneToOneField(User)
    company_name = models.CharField(max_length=50)

class Vend(models.Model):
    vendor = models.ForeignKey(Vendor)
    phone_number = models.CharField(max_length=10)
    voucher_id = models.PositiveSmallIntegerField()
    vend_date = models.DateTimeField(default=timezone.now)