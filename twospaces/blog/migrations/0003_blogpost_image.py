# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150506_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(upload_to='blog_images/%Y-%m', null=True, blank=True),
        ),
    ]
