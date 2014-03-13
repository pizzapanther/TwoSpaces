from django.contrib import admin
from django.db import models

from .models import Conference, SponsorshipLevel, Sponsor
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
  
admin.site.register(Conference, ConferenceAdmin)
admin.site.register(SponsorshipLevel, SponsorshipLevelAdmin)
admin.site.register(Sponsor, SponsorAdmin)
