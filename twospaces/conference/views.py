from django import http
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie

from twospaces.profiles.decorators import login_required, speaker_info_required

from .forms import SponsorForm, SessionForm
from .models import Conference, Session, Invoice

import stripe
stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')

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
  
def conference_proposed_talks (request, slug):
  templates = (
    'conference/{}/proposed-talks.html'.format(request.conference['slug']),
    'conference/proposed-talks.html'
  )
  
  sessions = Session.objects.filter(conference__id=request.conference['id']).order_by('name').select_related()
  
  c = {
    'title': 'Proposed Talks',
    'sessions': sessions
  }
  return TemplateResponse(request, templates, context=c)
  
@ensure_csrf_cookie
def invoice (request, key):
  invoice = get_object_or_404(Invoice, key=key, paid_on__isnull=True)
  
  if request.POST:
    invoice.paid_on = timezone.now()
    invoice.stripe_token = request.POST.get('stripeToken')
    charge = stripe.Charge.create(
      amount=invoice.cents(),
      currency="usd",
      card=invoice.stripe_token,
      description=invoice.name
    )
    invoice.stripe_charge = charge['id']
    invoice.save()
    
    templates = (
      'conference/invoice-success.html'
    )
    
  else:
    templates = (
      'conference/invoice.html'
    )
  
  c = {
    'title': invoice.name,
    'invoice': invoice
  }
  return TemplateResponse(request, templates, context=c)
  