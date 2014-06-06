from django import http
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage
from django.template.response import TemplateResponse

from twospaces.profiles.decorators import login_required, speaker_info_required

from .forms import SponsorForm, SessionForm
from .models import Conference

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
  
@login_required
@speaker_info_required
def conference_submit_talk (request, slug):
  templates = (
    'conference/{}/submit-talk.html'.format(request.conference['slug']),
    'conference/submit-talk.html'
  )
  
  form = SessionForm(request.POST or None)
  if request.POST:
    if form.is_valid():
      session = form.save(commit=False)
      session.set_duration()
      session.user = request.user
      session.conference_id = request.conference['id']
      session.save()
      
      session.send_submitted(request)
      
      return http.HttpResponseRedirect(reverse('conference-submit-talk-success', args=(request.conference['slug'],)))
      
  context = {
    'form': form,
    'title': 'Submit A Talk',
  }
  return TemplateResponse(request, templates, context)
  
def conference_submit_talk_success (request, slug):
  templates = (
    'conference/{}/submit-talk-success.html'.format(request.conference['slug']),
    'conference/submit-talk-success.html'
  )
  
  return TemplateResponse(request, templates, context = {'title': 'Talk Submission Successful'})
  