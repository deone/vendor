# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vend', '0003_vend'),
    ]

    operations = [
        migrations.AddField(
            model_name='vend',
            name='voucher_type',
            field=models.CharField(default='STD', max_length=3, choices=[(b'', b'Select Type'), (b'STD', b'Standard'), (b'INS', b'Instant')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vend',
            name='voucher_value',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vend',
            name='voucher_id',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
