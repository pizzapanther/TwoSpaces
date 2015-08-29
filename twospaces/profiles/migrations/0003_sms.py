# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20150413_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('to', models.CharField(max_length=50)),
                ('frm', models.CharField(max_length=50, verbose_name='From')),
                ('message', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('reply_to', models.ForeignKey(blank=True, null=True, to='profiles.SMS')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
