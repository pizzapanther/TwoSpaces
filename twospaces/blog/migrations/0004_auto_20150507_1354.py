# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogpost_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'get_latest_by': 'publish', 'ordering': ('-publish',)},
        ),
    ]
