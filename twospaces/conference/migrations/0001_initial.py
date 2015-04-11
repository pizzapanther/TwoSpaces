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
            name='Conference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True)),
                ('logo', models.ImageField(upload_to='conf_logos/%Y-%m/', null=True, blank=True)),
                ('favicon', models.ImageField(upload_to='conf_logos/%Y-%m/', null=True, blank=True)),
                ('banner_logo', models.ImageField(upload_to='conf_logos/%Y-%m/', null=True, blank=True)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('registration_open', models.DateTimeField()),
                ('registration_closed', models.DateTimeField()),
                ('cfp_open', models.DateTimeField(null=True, verbose_name='Call for Proposals Open', blank=True)),
                ('cfp_closed', models.DateTimeField(null=True, verbose_name='Call for Proposals Closed', blank=True)),
                ('active', models.BooleanField()),
            ],
            options={
                'ordering': ('-start',),
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.EmailField(max_length=254)),
                ('key', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=255, verbose_name='Transaction Name')),
                ('subject', models.CharField(max_length=255)),
                ('text', models.TextField(help_text='Link will be generated by the invoice system.', default='Follow the link below to complete your sponsorship transaction.')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('sent', models.DateTimeField(null=True, blank=True)),
                ('stripe_token', models.CharField(max_length=255, null=True, blank=True)),
                ('stripe_charge', models.CharField(max_length=255, null=True, blank=True)),
                ('paid_on', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-sent',),
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sorder', models.IntegerField(verbose_name='Order')),
                ('conference', models.ForeignKey(to='conference.Conference')),
            ],
            options={
                'ordering': ('sorder',),
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all_rooms', models.BooleanField(default=False)),
                ('video', models.BooleanField(default=True, verbose_name='Make recording')),
                ('name', models.CharField(max_length=100, verbose_name='Title of Talk')),
                ('description', models.TextField()),
                ('slides', models.URLField(null=True, verbose_name='URL To Presentation', blank=True)),
                ('stype', models.CharField(max_length=25, choices=[('lightning', 'Lightning Talk (5 Minutes)'), ('talk-short', 'Short Talk (25 Minutes)'), ('talk-long', 'Talk (50 Minutes)'), ('tutorial', 'Tutorial (3 Hours)'), ('non-talk', 'Non Talk')], verbose_name='Session Type')),
                ('level', models.CharField(max_length=25, choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], verbose_name='Audience Level')),
                ('status', models.CharField(max_length=25, choices=[('submitted', 'Submitted'), ('maybe', 'Maybe'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='submitted')),
                ('start', models.DateTimeField(null=True, blank=True)),
                ('duration', models.IntegerField(help_text='Time in Minutes', null=True, blank=True)),
                ('special_requirements', models.TextField(help_text='If you require any special equipment or materials, please let us know here.', null=True, blank=True)),
                ('conference', models.ForeignKey(to='conference.Conference')),
                ('room', models.ForeignKey(to='conference.Room', blank=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('start',),
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField(verbose_name='URL')),
                ('description', models.TextField(blank=True)),
                ('contact_name', models.CharField(max_length=100, null=True, blank=True)),
                ('contact_phone', models.CharField(max_length=100, null=True, blank=True)),
                ('contact_email', models.EmailField(max_length=254, null=True, blank=True)),
                ('active', models.BooleanField()),
                ('logo', models.ImageField(upload_to='sponsor_logos/%Y-%m/', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SponsorshipLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cost', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True)),
                ('order', models.IntegerField(default=0)),
                ('conference', models.ForeignKey(to='conference.Conference')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.AddField(
            model_name='sponsor',
            name='level',
            field=models.ForeignKey(to='conference.SponsorshipLevel'),
        ),
    ]
