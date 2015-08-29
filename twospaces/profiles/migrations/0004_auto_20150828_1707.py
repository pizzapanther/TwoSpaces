# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_sms'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sms',
            options={'ordering': ('-created',), 'verbose_name_plural': "SMS's"},
        ),
        migrations.AddField(
            model_name='sms',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
