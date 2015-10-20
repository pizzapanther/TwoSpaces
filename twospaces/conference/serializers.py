from rest_framework import serializers

from twospaces.conference.models import Session, Conference, SponsorshipLevel, Sponsor, Room
from twospaces.profiles.models import User
from twospaces.profiles.serializers import UserPublicSizzler
from twospaces.utils import DynamicFieldsMixin


class ProposedReadSizzler(DynamicFieldsMixin, serializers.ModelSerializer):
  user = UserPublicSizzler(exclude=('biography', 'website', 'social_handles'))
  level = serializers.CharField(source='get_level_display', read_only=True)
  stype = serializers.CharField(source='get_stype_display', read_only=True)

  class Meta:
    model = Session
    fields = ('id', 'user', 'name', 'description', 'level', 'stype', 'slides',
              'video_url', 'start', 'duration')
    read_only_fields = fields


class SessionSizzler(DynamicFieldsMixin, serializers.ModelSerializer):

  class Meta:
    model = Session
    fields = ('name', 'description', 'level', 'stype', 'slides', 'video_url',
              'special_requirements')


class ConferenceReadSizzler(DynamicFieldsMixin, serializers.ModelSerializer):

  class Meta:
    model = Conference
    fields = ('name', 'slug', 'start', 'end', 'registration_open',
              'registration_closed', 'cfp_open', 'cfp_closed')
    read_only_fields = fields


class SponsorSizzler(DynamicFieldsMixin, serializers.ModelSerializer):

  class Meta:
    model = Sponsor
    fields = ('name', 'url', 'logo')
    read_only_fields = fields


class SponsorshipLevelSizzler(DynamicFieldsMixin, serializers.ModelSerializer):
  sponsors = SponsorSizzler(many=True)

  class Meta:
    model = SponsorshipLevel
    fields = ('name', 'sponsors')
    read_only_fields = fields


class RoomSizzler(serializers.ModelSerializer):

  class Meta:
    model = Room
    fields = ('name',)


class UserSizzler(DynamicFieldsMixin, serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ('username', 'name')
    read_only_fields = fields


class SessionScheduleSizzler(serializers.ModelSerializer):
  room = RoomSizzler()
  user = UserSizzler()

  class Meta:
    model = Session
    fields = (
        'id', 'name', 'level', 'stype', 'all_rooms', 'room', 'start', 'end',
        'duration', 'user')


class SessionPyVideoSizzler(serializers.ModelSerializer):
  room = RoomSizzler()
  speaker = UserSizzler(source='user')
  type = serializers.CharField(source='get_stype_display')
  make_recording = serializers.BooleanField(source='video')
  released = serializers.BooleanField()
  slides_url = serializers.CharField(source='slides')
  url = serializers.CharField()

  class Meta:
    model = Session
    fields = (
        'id', 'name', 'description', 'type', 'room', 'start', 'end', 'url',
        'duration', 'speaker', 'make_recording', 'released', 'license',
        'language', 'video_url', 'slides_url')
