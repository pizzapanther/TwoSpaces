# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0004_auto_20150429_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='video_url',
            field=models.URLField(null=True, blank=True, verbose_name='URL To Video'),
        ),
    ]
