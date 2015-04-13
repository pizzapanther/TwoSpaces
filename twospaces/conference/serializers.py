from rest_framework import serializers

from twospaces.conference.models import Session
from twospaces.profiles.serializers import UserPublicSizzler

class ProposedReadSizzler (serializers.ModelSerializer):
  user = UserPublicSizzler()
  
  class Meta:
    model = Session
    fields = ('id', 'user', 'name', 'description', 'level')
    read_only_fields = fields
    