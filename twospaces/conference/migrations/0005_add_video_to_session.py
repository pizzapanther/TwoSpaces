# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0004_auto_20150429_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='conference',
            field=models.ForeignKey(to='conference.Conference'),
        ),
        migrations.AlterField(
            model_name='session',
            name='video',
            field=models.URLField(null=True, verbose_name=b'URL To Video', blank=True),
        ),
    ]
