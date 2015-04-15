# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0002_auto_20150411_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='stype',
            field=models.CharField(verbose_name='Session Type', choices=[('lightning', 'Lightning Talk (5 Minutes)'), ('talk-short', 'Short Talk (20 Minutes)'), ('talk-long', 'Talk (45 Minutes)'), ('tutorial', 'Tutorial (3 Hours)'), ('non-talk', 'Non Talk')], max_length=25),
        ),
    ]
