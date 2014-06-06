from django.contrib import admin
from django.db import models

from .models import Conference, SponsorshipLevel, Sponsor, Session
from ..widgets import RichText

class ConferenceAdmin (admin.ModelAdmin):
  list_display = ('name', 'default', 'slug', 'start', 'end', 'active', 'registration_open', 'registration_closed')
  list_filter = ('active',)
  list_editable = ('active',)
  search_fields = ('name', )
  date_hierarchy = 'start'
  
  formfield_overrides = {
    models.TextField: {'widget': RichText},
  }
  
class SponsorshipLevelAdmin (admin.ModelAdmin):
  list_display = ('name', 'conference', 'cost', 'order')
  list_filter = ('conference',)
  list_editable = ('order',)
  raw_id_fields = ('conference',)
  autocomplete_lookup_fields = {
    'fk': ['conference'],
  }
  
class SponsorAdmin (admin.ModelAdmin):
  list_display = ('name', 'level', 'contact_name', 'contact_phone', 'contact_email', 'link', 'active')
  list_filter = ('level', 'active')
  list_editable = ('active',)
  raw_id_fields = ('level',)
  autocomplete_lookup_fields = {
    'fk': ['level'],
  }
  
class SessionAdmin (admin.ModelAdmin):
  list_display = ('name', 'conference', 'user', 'stype', 'level', 'start', 'duration', 'status')
  list_filter = ('conference', 'stype', 'level', 'status')
  list_editable = ('status',)
  raw_id_fields = ('user',)
  autocomplete_lookup_fields = {
    'fk': ['user'],
  }
  
  formfield_overrides = {
    models.TextField: {'widget': RichText},
  }
  
admin.site.register(Conference, ConferenceAdmin)
admin.site.register(SponsorshipLevel, SponsorshipLevelAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Session, SessionAdmin)
