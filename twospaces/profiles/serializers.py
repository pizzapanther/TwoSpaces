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
    
class UserSizzler (DynamicFieldsMixin, serializers.ModelSerializer):
  social_handles = SocialHandleSizzler(many=True, required=False)
  
  class Meta:
    model = User
    fields = ('username', 'email', 'password', 'name', 'image', 'biography', 'website', 'social_handles', 'phone')
    extra_kwargs = {'password': {'write_only': True}}
    
  def create (self, validated_data):
    kwargs = {}
    for f in self.fields:
      if f != 'social_handles' and f != 'password':
        value = validated_data.get(f, None)
        if value:
          kwargs[f] = value
          
    instance = User(**kwargs)
    instance.save()
    
    if 'social_handles' in validated_data:
      for handle in validated_data['social_handles']:
        h = SocialHandle(user=instance, username=handle['username'], site=handle['site'])
        h.save()
        
    return instance
    
class UserUpdateSizzler (UserSizzler):
  class Meta:
    model = User
    fields = ('username', 'email', 'password', 'name', 'first_name', 'last_name', 'image', 'biography', 'website', 'social_handles', 'phone')
    extra_kwargs = {'password': {'write_only': True, 'required': False}}
    
  def update (self, instance, validated_data):
    for f in self.fields:
      if f != 'social_handles' and f != 'password':
        value = validated_data.get(f, getattr(instance, f))
        setattr(instance, f, value)
        
    instance.save()
    instance.social_handles.all().delete()
    
    if 'social_handles' in validated_data:
      for handle in validated_data['social_handles']:
        h = SocialHandle(user=instance, username=handle['username'], site=handle['site'])
        h.save()
        
    return instance
    