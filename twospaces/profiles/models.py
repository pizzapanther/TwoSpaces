from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser

class User (AbstractUser):
  verified_email = models.EmailField(null=True, blank=True)
  biography = models.TextField(null=True, blank=True)
  website = models.URLField(null=True, blank=True)
  
  photo = models.ImageField(upload_to="user_photos/%Y-%m", blank=True, null=True)
  avatar = models.ImageField(upload_to="user_photos/%Y-%m", blank=True, null=True)
  
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

class SocialHandle (models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  username = models.CharField(max_length=35)
  site = models.CharField(max_length=25, choices=SOCIAL_SITES)
  