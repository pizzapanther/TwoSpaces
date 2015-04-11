# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conference',
            name='banner_logo',
        ),
        migrations.RemoveField(
            model_name='conference',
            name='description',
        ),
        migrations.RemoveField(
            model_name='conference',
            name='favicon',
        ),
        migrations.RemoveField(
            model_name='conference',
            name='logo',
        ),
    ]
