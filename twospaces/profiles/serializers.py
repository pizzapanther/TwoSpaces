from rest_framework import serializers

from twospaces.profiles.models import User

class UserPublicSizzler (serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'name', 'image')
    read_only_fields = fields
    