from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.cache import get_cache

cache = get_cache('default')

class ActiveManager (models.Manager):
  def get_queryset (self):
    return super(ActiveManager, self).get_queryset().filter(active=True)
    
class Conference (models.Model):
  name = models.CharField(max_length=100)
  slug = models.SlugField()
  description = models.TextField(blank=True)
  
  logo = models.ImageField(upload_to="conf_logos/%Y-%m/", blank=True, null=True)
  favicon = models.ImageField(upload_to="conf_logos/%Y-%m/", blank=True, null=True)
  banner_logo = models.ImageField(upload_to="conf_logos/%Y-%m/", blank=True, null=True)
  
  start = models.DateField()
  end = models.DateField()
  
  registration_open = models.DateTimeField()
  registration_closed = models.DateTimeField()
  
  active = models.BooleanField()
  default = models.BooleanField()
  
  objects = models.Manager()
  live = ActiveManager()
  
  class Meta:
    ordering = ('-start',)
    
  def __unicode__ (self):
    return self.name
    
  @staticmethod
  def autocomplete_search_fields():
    return ("id__iexact", "name__icontains", "slug__icontains")
    
CONF_LIST_KEY = 'TWOSPACES-CONFS'
def get_set_conferences (force=False):
  confs = cache.get(CONF_LIST_KEY)
  if not confs or force:
    confs = Conference.live.all().values()
    cache.set(CONF_LIST_KEY, confs)
    
  return confs
  
@receiver(post_save, sender=Conference, dispatch_uid='conf_post_save')
def update_default_conf (sender, instance, **kwargs):
  if instance.default:
    Conference.objects.exclude(id=instance.id).update(default=False)
    
  get_set_conferences(True)
  
class SponsorshipLevel (models.Model):
  conference = models.ForeignKey(Conference)
  
  name = models.CharField(max_length=100)
  cost = models.PositiveIntegerField()
  description = models.TextField(blank=True)
  
  order = models.IntegerField(default=0)
  
  class Meta:
    ordering = ("order",)
    
  def __unicode__ (self):
    return '{} {}'.format(self.name, self.conference.slug)
    
  @staticmethod
  def autocomplete_search_fields():
    return ("id__iexact", "name__icontains")
    
  def sponsors (self):
    return self.sponsor_set.filter(active=True)
    
class Sponsor (models.Model):
  name = models.CharField(max_length=100)
  url = models.URLField('URL')
  description = models.TextField(blank=True)
  
  contact_name = models.CharField(max_length=100, blank=True, null=True)
  contact_phone = models.CharField(max_length=100, blank=True, null=True)
  contact_email = models.EmailField(blank=True, null=True)
  
  level = models.ForeignKey(SponsorshipLevel)
  
  active = models.BooleanField()
  
  logo = models.ImageField(upload_to="sponsor_logos/%Y-%m/", blank=True, null=True)
  
  def __unicode__ (self):
    return self.name
    
  def link (self):
    return '<a href="{}" target="_blank">Webpage &raquo;</a>'.format(self.url)
    
  link.allow_tags = True
  