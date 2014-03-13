from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.dispatch import receiver
from django.db.models.signals import post_save

class User (AbstractUser):
  verified_email = models.EmailField(null=True, blank=True,
    help_text="If doesn't match e-mail field then user is sent a link to verify address.")
  biography = models.TextField(null=True, blank=True)
  website = models.URLField(null=True, blank=True)
  
  photo = models.ImageField(upload_to="user_photos/%Y-%m", blank=True, null=True)
  avatar = models.ImageField(upload_to="user_photos/%Y-%m", blank=True, null=True)
  
  def __unicode__ (self):
    return self.username
    
emailField = User._meta.get_field('email')
emailField._unique = True
emailField.blank = False

@receiver(post_save, sender=User, dispatch_uid='user_post_save')
def send_verify_email (sender, instance, **kwargs):
  if instance.email != instance.verified_email:
    pass
    #send verified email
    
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
    