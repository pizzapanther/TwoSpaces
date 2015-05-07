from django import http
from django.conf import settings
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from twospaces.blog.models import Category, BlogPost

def blog_rss (request):
  category = request.GET.get('category', None)
  
  qs = BlogPost.published.all()
  if category is not None:
    category = get_object_or_404(Category, slug=category)
    qs = qs.filter(categories=category)
    
  context = {
    'posts': qs[:25],
    'category': category,
    'conf': settings.DEFAULT_CONF,
  }
  return TemplateResponse(
    request,
    'blog/index.atom.xml',
    context,
    content_type='application/atom+xml'
  )
  