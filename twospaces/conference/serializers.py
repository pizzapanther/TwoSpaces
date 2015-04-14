from rest_framework import serializers

from twospaces.conference.models import Session
from twospaces.profiles.serializers import UserPublicSizzler
from twospaces.utils import DynamicFieldsMixin

class ProposedReadSizzler (DynamicFieldsMixin, serializers.ModelSerializer):
  user = UserPublicSizzler(exclude=('biography', 'website', 'social_handles'))
  level = serializers.CharField(source='get_level_display', read_only=True)
  stype = serializers.CharField(source='get_stype_display', read_only=True)
  
  class Meta:
    model = Session
    fields = ('id', 'user', 'name', 'description', 'level', 'stype', 'slides', 'start', 'duration')
    read_only_fields = fields
    
class SessionSizzler (DynamicFieldsMixin, serializers.ModelSerializer):
  class Meta:
    model = Session
    fields = ('name', 'description', 'level', 'stype', 'slides', 'special_requirements')
    