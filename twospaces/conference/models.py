from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.cache import get_cache
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail

cache = get_cache('default')

from ..settings import SPONSOR_NOTIFY, SPEAKER_NOTIFY

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
  
  def notify (self):
    if SPONSOR_NOTIFY:
      c = {
        'sponsor': self
      }
      
      slug = self.level.conference.slug
      text_templates = (
        'conference/{}/sponsor-notify.email.txt'.format(slug),
        'conference/sponsor-notify.email.txt'
      )
      html_templates = (
        'conference/{}/sponsor-notify.email.html'.format(slug),
        'conference/sponsor-notify.email.html'
      )
      
      text = render_to_string(text_templates, c)
      html = render_to_string(html_templates, c)
      
      msg = EmailMultiAlternatives('New Sponsor', text, settings.DEFAULT_FROM_EMAIL, SPONSOR_NOTIFY)
      msg.attach_alternative(html, "text/html")
      msg.send()
      
SESSION_TYPES = (
  ('lightning', 'Lightning Talk (5 Minutes)'),
  ('talk-short', 'Short Talk (25 Minutes)'),
  ('talk-long', 'Talk (50 Minutes)'),
  ('tutorial', 'Tutorial (3 Hours)'),
)

SESSION_LENGTH = {
  'lightning': 5,
  'talk-short': 25,
  'talk-long': 50,
  'tutorial': 180,
}

SESSION_STATUS = (
  ('submitted', 'Submitted'),
  ('maybe', 'Maybe'),
  ('accepted', 'Accepted'),
  ('declined', 'Declined'),
)

SESSION_LEVELS = (
  ('beginner', 'Beginner'),
  ('intermediate', 'Intermediate'),
  ('advanced', 'Advanced'),
)

class Session (models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  conference = models.ForeignKey(Conference)
  
  name = models.CharField('Title of Talk', max_length=100)
  description = models.TextField()
  
  stype = models.CharField('Session Type', max_length=25, choices=SESSION_TYPES)
  level = models.CharField('Audience Level', max_length=25, choices=SESSION_LEVELS)
  
  status = models.CharField(max_length=25, choices=SESSION_STATUS, default='submitted')
  
  start = models.DateTimeField(blank=True, null=True)
  duration = models.IntegerField(blank=True, null=True, help_text="Time in Minutes")
  
  special_requirements = models.TextField(blank=True, null=True, help_text="If you require any special equipment or materials, please let us know here.")
  
  def __unicode__ (self):
    return self.name
    
  def set_duration (self):
    self.duration = SESSION_LENGTH[self.stype]
    
  class Meta:
    ordering = ("start",)
    
  def send_submitted (self, request):
    subject = "Talk Submission - {}".format(self.user.__unicode__())
    message = render_to_string('conference/email.talk-submission.txt', {'request': request, 'session': self})
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, SPEAKER_NOTIFY, fail_silently=False)
    