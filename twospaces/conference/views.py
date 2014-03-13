from django import http
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage
from django.template.response import TemplateResponse

def favicon (request):
  if request.conference and request.conference['favicon']:
    return http.HttpResponseRedirect(default_storage.url(request.conference['favicon']))
    
  raise http.Http404
  
def home_redirect (request):
  if request.conference:
    return http.HttpResponseRedirect(reverse('conference-home', args=(request.conference['slug'],)))
    
  raise http.Http404
  
def conference_home (request, slug):
  templates = ('conference/{}/home.html'.format(request.conference['slug']), 'conference/home.html')
  context = {
    'conference': request.conference,
    'home': True,
  }
  return TemplateResponse(request, templates, context)
  