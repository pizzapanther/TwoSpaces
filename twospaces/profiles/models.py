import random
import hashlib

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.template.loader import render_to_string

class User (AbstractUser):
  verified_email = models.EmailField(null=True, blank=True,
    help_text="If doesn't match e-mail field then user is sent a link to verify address.")
  biography = models.TextField(null=True, blank=True, help_text="Markdown formatted text accepted.")
  website = models.URLField(null=True, blank=True)
  
  avatar = models.ImageField(upload_to="user_photos/%Y-%m", blank=True, null=True)
  
  phone = models.CharField(blank=True, null=True, max_length=25)
  
  def __unicode__ (self):
    return self.username
    
  def send_verify (self, site):
    if not self.verified_email or self.email.lower() != self.verified_email.lower():
      ev = EmailVerification.create_verify(self)
      subject = "Please verify your address - {}".format(settings.SITE_NAME)
      message = render_to_string('profiles/email.verification.txt', {'ev': ev, 'site': site})
      send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [ev.sent_to], fail_silently=False)
      
  @staticmethod
  def autocomplete_search_fields ():
    return ("id__iexact", "username__icontains", "first_name__icontains", "last_name__icontains", "email__icontains")
    
emailField = User._meta.get_field('email')
emailField._unique = True
emailField.blank = False

SOCIAL_SITES = (
  ('about.me', 'About.Me'),
  ('facebook', 'Facebook'),
  ('github', 'Github'),
  ('gplus', 'Google+'),
  ('twitter', 'Twitter'),
)

SOCIAL_INFO = {
  'about.me': {'domain': 'about.me/', 'icon': 'fa-user'},
  'facebook': {'domain': 'facebook.com/', 'icon': 'fa-facebook-square'},
  'github': {'domain': 'github.com/', 'icon': 'fa-github-square'},
  'gplus': {'domain': 'plus.google.com/+', 'icon': 'fa-google-plus-square'},
  'twitter': {'domain': 'twitter.com/', 'icon': 'fa-twitter-square'},
}

class SocialHandle (models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  username = models.CharField(max_length=35)
  site = models.CharField(max_length=25, choices=SOCIAL_SITES)
  
  class Meta:
    ordering = ('site',)
    
  def __unicode__ (self):
    return '{}: {}'.format(self.get_site_display(), self.username)
    
  def link (self):
    domain = SOCIAL_INFO[self.site]['domain']
    return 'http://{}{}'.format(domain, self.username)
    
  def icon (self):
    return SOCIAL_INFO[self.site]['icon']
    
class EmailVerification (models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  sent_to = models.EmailField()
  secret = models.CharField(max_length=255, unique=True)
  used = models.BooleanField(default=False)
  
  created = models.DateTimeField(auto_now_add=True)
  
  @classmethod
  def create_verify (cls, user):
    while 1:
      salt = hashlib.sha256(str(random.random())).hexdigest()[:5]
      ck = hashlib.sha256(salt + user.email).hexdigest()
      ev = cls(user=user, secret=ck, sent_to=user.email)
      
      try:
        ev.save()
        
      except:
        pass
        
      else:
        break
        
    return ev