from rest_framework import serializers

from twospaces.conference.models import Session, Conference, SponsorshipLevel, Sponsor
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
    
class ConferenceReadSizzler (DynamicFieldsMixin, serializers.ModelSerializer):
  class Meta:
    model = Conference
    fields = ('name', 'slug', 'start', 'end', 'registration_open', 
              'registration_closed', 'cfp_open', 'cfp_closed')
    read_only_fields = fields
    
class SponsorSizzler (DynamicFieldsMixin, serializers.ModelSerializer):
  class Meta:
    model = Sponsor
    fields = ('name', 'url', 'logo')
    read_only_fields = fields
    
class SponsorshipLevelSizzler (DynamicFieldsMixin, serializers.ModelSerializer):
  sponsors = SponsorSizzler(many=True)
  
  class Meta:
    model = SponsorshipLevel
    fields = ('name', 'sponsors')
    read_only_fields = fields
    