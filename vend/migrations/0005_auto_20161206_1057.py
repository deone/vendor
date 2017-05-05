# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vend', '0004_auto_20161205_1713'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vend',
            old_name='phone_number',
            new_name='subscriber_phone_number',
        ),
        migrations.AddField(
            model_name='vendor',
            name='phone_number',
            field=models.CharField(default='0231802940', max_length=10),
            preserve_default=False,
        ),
    ]
