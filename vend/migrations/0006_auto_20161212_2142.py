# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-12 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vend', '0005_auto_20161206_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vend',
            name='voucher_value',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]
