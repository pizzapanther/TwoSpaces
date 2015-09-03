from rest_framework import serializers

from twospaces.profiles.serializers import UserPublicSizzler
from twospaces.utils import DynamicFieldsMixin
from twospaces.blog.models import BlogPost, Category


class CategorySerializer(serializers.ModelSerializer):

  class Meta:
    model = Category
    fields = ('title', 'slug')
    read_only_fields = fields


class PostSizzler(DynamicFieldsMixin, serializers.ModelSerializer):
  categories = CategorySerializer(many=True)
  authors = UserPublicSizzler(
      many=True,
      exclude=('biography', 'website', 'social_handles'))
  thumbnail = serializers.CharField(source='get_thumbnail')

  class Meta:
    model = BlogPost
    fields = ('id', 'title', 'slug', 'image', 'thumbnail', 'body', 'authors',
              'publish', 'categories')
    read_only_fields = fields
