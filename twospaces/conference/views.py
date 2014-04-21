from django import http
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage
from django.template.response import TemplateResponse

from .forms import SponsorForm

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
  
def conference_sponsor (request, slug):
  templates = (
    'conference/{}/sponsor.html'.format(request.conference['slug']),
    'conference/sponsor.html'
  )
  
  form = SponsorForm(request.conference['id'])
  if request.POST:
    form = SponsorForm(request.conference['id'], request.POST, request.FILES)
    
    if form.is_valid():
      sponsor = form.save(commit=False)
      sponsor.active = False
      sponsor.save()
      sponsor.notify()
      templates = (
        'conference/{}/sponsor-thankyou.html'.format(request.conference['slug']),
        'conference/sponsor-thankyou.html'
      )
      
  context = {
    'form': form,
  }
  return TemplateResponse(request, templates, context)
  