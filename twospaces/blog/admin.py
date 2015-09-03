from django.contrib import admin
from django.db import models

from twospaces.widgets import RichText
from twospaces.blog.models import Category, BlogPost


class CatAdmin(admin.ModelAdmin):
  list_display = ('title', 'slug')
  search_fields = ('title', 'slug')


class PostAdmin(admin.ModelAdmin):
  list_display = ('title', 'slug', 'Categories', 'Authors', 'publish')
  search_fields = ('title', 'slug')
  list_filter = ('authors', 'categories')
  date_hierarchy = 'publish'
  raw_id_fields = ('categories', 'authors')
  autocomplete_lookup_fields = {'m2m': ['categories', 'authors'],}

  formfield_overrides = {models.TextField: {'widget': RichText},}

  def Categories(self, obj):
    ret = ''
    for c in obj.categories.all():
      ret += c.title + ', '

    if ret:
      return ret[:-2]

    return ret

  def Authors(self, obj):
    ret = ''
    for c in obj.authors.all():
      ret += c.username + ', '

    if ret:
      return ret[:-2]

    return ret


admin.site.register(Category, CatAdmin)
admin.site.register(BlogPost, PostAdmin)
