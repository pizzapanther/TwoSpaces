# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Sponsor.large_logo'
        db.delete_column(u'conference_sponsor', 'large_logo')

        # Deleting field 'Sponsor.small_logo'
        db.delete_column(u'conference_sponsor', 'small_logo')

        # Adding field 'Sponsor.logo'
        db.add_column(u'conference_sponsor', 'logo',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Sponsor.large_logo'
        db.add_column(u'conference_sponsor', 'large_logo',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Sponsor.small_logo'
        db.add_column(u'conference_sponsor', 'small_logo',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Sponsor.logo'
        db.delete_column(u'conference_sponsor', 'logo')


    models = {
        u'conference.conference': {
            'Meta': {'ordering': "('-start',)", 'object_name': 'Conference'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'banner_logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end': ('django.db.models.fields.DateField', [], {}),
            'favicon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'registration_closed': ('django.db.models.fields.DateTimeField', [], {}),
            'registration_open': ('django.db.models.fields.DateTimeField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        u'conference.sponsor': {
            'Meta': {'object_name': 'Sponsor'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conference.SponsorshipLevel']"}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'conference.sponsorshiplevel': {
            'Meta': {'ordering': "('order',)", 'object_name': 'SponsorshipLevel'},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['conference.Conference']"}),
            'cost': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['conference']