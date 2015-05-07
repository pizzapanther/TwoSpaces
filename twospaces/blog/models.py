from django.db import models
from django.utils import timezone

import markdown as markdown_module
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize

class Category (models.Model):
  title = models.CharField(max_length=100)
  slug = models.SlugField(unique=True, max_length=200)
  
  @staticmethod
  def autocomplete_search_fields():
    return ("id__iexact", "title__icontains")
    
  class Meta:
    ordering = ('slug',)
    verbose_name_plural = 'Categories'
    
  def __str__ (self):
    return self.title
    
class PublishedManager (models.Manager):
  def get_queryset (self):
    qs = super(PublishedManager, self).get_queryset()
    qs = qs.filter(publish__lte=timezone.now())
    
    return qs
    
class BlogPost (models.Model):
  title = models.CharField(max_length=255)
  slug = models.SlugField(unique=True, max_length=200)
  authors = models.ManyToManyField('profiles.User', blank=True)
  publish = models.DateTimeField()
  categories = models.ManyToManyField(Category, blank=True)
  
  image = models.ImageField(upload_to="blog_images/%Y-%m", blank=True, null=True)
  image_thumbnail = ImageSpecField(source='image',
                                    processors=[SmartResize(128, 128)],
                                    format='JPEG',
                                    options={'quality': 90}
                                  )
  body = models.TextField()
  
  objects = models.Manager()
  published = PublishedManager()
  
  @staticmethod
  def autocomplete_search_fields():
    return ("id__iexact", "title__icontains", "slug__icontains")
    
  class Meta:
    ordering = ('-publish',)
    
  def __str__ (self):
    return self.title
    
  def related (self, num=5):
    cats = self.categories.all()
    return Post.objects.filter(categories__in=cats).exclude(id=self.id).distinct()[:num]
    
  def body_html (self):
    return markdown_module.markdown(self.body)
    
  def get_thumbnail (self):
    if self.image:
      return self.image_thumbnail.url
      
    return None
    