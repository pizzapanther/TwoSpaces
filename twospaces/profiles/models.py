import random
import hashlib

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

class User (AbstractUser):
  verified_email = models.EmailField(null=True, blank=True,
    help_text="If doesn't match e-mail field then user is sent a link to verify address.")
  biography = models.TextField(null=True, blank=True)
  website = models.URLField(null=True, blank=True)
  
  avatar = models.ImageField(upload_to="user_photos/%Y-%m", blank=True, null=True)
  
  phone = models.CharField(blank=True, null=True, max_length=25)
  
  def __unicode__ (self):
    return self.username
    
emailField = User._meta.get_field('email')
emailField._unique = True
emailField.blank = False

@receiver(post_save, sender=User, dispatch_uid='user_post_save')
def send_verify_email (sender, instance, **kwargs):
  if not instance.verified_email or instance.email.lower() != instance.verified_email.lower():
    ev = EmailVerification.create_verify(instance)
    subject = "Please verify your address - {}".format(settings.SITE_NAME)
    site = Site.objects.get(id=settings.SITE_ID)
    message = render_to_string('profiles/email.verification.txt', {'ev': ev, 'site': site})
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [ev.sent_to], fail_silently=False)
    
SOCIAL_SITES = (
  ('about.me', 'About.Me'),
  ('facebook', 'Facebook'),
  ('github', 'Github'),
  ('gplus', 'Google+'),
  ('twitter', 'Twitter'),
)

class SocialHandle (models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  username = models.CharField(max_length=35)
  site = models.CharField(max_length=25, choices=SOCIAL_SITES)
  
  class Meta:
    ordering = ('site',)
    
  def __unicode__ (self):
    return '{}: {}'.format(self.get_site_display(), self.username)
    
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