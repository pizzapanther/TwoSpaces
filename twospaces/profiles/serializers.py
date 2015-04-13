from rest_framework import serializers

from twospaces.utils import DynamicFieldsMixin
from twospaces.profiles.models import User, SocialHandle

class SocialHandleSizzler (DynamicFieldsMixin, serializers.ModelSerializer):
  class Meta:
    model = SocialHandle
    fields = ('username', 'site')
    
class UserPublicSizzler (DynamicFieldsMixin, serializers.ModelSerializer):
  social_handles = SocialHandleSizzler(many=True)
  
  class Meta:
    model = User
    fields = ('username', 'name', 'image', 'biography', 'website', 'social_handles')
    read_only_fields = fields
    