# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vend', '0002_auto_20151123_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=10)),
                ('voucher_id', models.PositiveSmallIntegerField()),
                ('vend_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('vendor', models.ForeignKey(to='vend.Vendor')),
            ],
        ),
    ]
