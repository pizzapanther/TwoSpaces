# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('publish', models.DateTimeField()),
                ('body', models.TextField()),
                ('authors', models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, max_length=200)),
            ],
            options={
                'ordering': ('slug',),
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AddField(
            model_name='blogpost',
            name='categories',
            field=models.ManyToManyField(null=True, to='blog.Category', blank=True),
        ),
    ]
