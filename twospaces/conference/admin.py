import hashlib
import random
import datetime

from functools import update_wrapper

from django.contrib import admin
from django.db import models
from django import http

from .models import Conference, SponsorshipLevel, Sponsor, Session, Invoice
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
  list_display = ('name', 'conference', 'user', 'email', 'stype', 'level', 'start', 'duration', 'status')
  list_filter = ('conference', 'stype', 'level', 'status')
  list_editable = ('status',)
  raw_id_fields = ('user',)
  autocomplete_lookup_fields = {
    'fk': ['user'],
  }
  
  formfield_overrides = {
    models.TextField: {'widget': RichText},
  }
  
class InvoiceAdmin (admin.ModelAdmin):
  list_display = ('to', 'name', 'amount', 'paid_on', 'sent', 'Send', 'Payment')
  list_filter = ('paid_on',)
  date_hierarchy = 'sent'
  exclude = ('key',)
  
  def save_model (self, request, obj, form, change):
    if not obj.key:
      while 1:
        m = hashlib.md5()
        m.update(obj.to)
        m.update(obj.text)
        m.update(obj.subject)
        m.update(datetime.datetime.now().strftime("'%Y-%m-%d %H:%M:%S.%f"))
        m.update(unicode(random.randint(0, 100000000)))
        key = m.hexdigest()
        if Invoice.objects.filter(key=key).count() == 0:
          break
          
      obj.key = key
      
    obj.save()
    
  def get_urls (self):
    from django.conf.urls import patterns, url
    def wrap(view):
      def wrapper(*args, **kwargs):
        return self.admin_site.admin_view(view)(*args, **kwargs)
        
      return update_wrapper(wrapper, view)
      
    info = self.model._meta.app_label, self.model._meta.model_name
    
    urlpatterns = patterns('',
      url(r'^(\d+)/send/$', wrap(self.send_view), name='%s_%s_send' % info),
    )
    
    urlpatterns += super(InvoiceAdmin, self).get_urls()
    
    return urlpatterns
    
  def send_view (self, request, object_id):
    obj = self.get_object(request, object_id)
    obj.send(request)
    
    return http.HttpResponseRedirect('../../')
    
admin.site.register(Conference, ConferenceAdmin)
admin.site.register(SponsorshipLevel, SponsorshipLevelAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Invoice, InvoiceAdmin)
