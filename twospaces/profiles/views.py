import datetime

from django import http
from django.contrib.auth import logout
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.sites.models import get_current_site

from .forms import LoginForm, SignupForm, ProfileForm, SocialHandleFormSet
from .models import SocialHandle, EmailVerification
from .decorators import login_required

@ensure_csrf_cookie
def signup (request):
  initial = {}
  r = request.GET.get('redirect', '')
  if r:
    initial = {'redirect': r}
    
  form = SignupForm(request.POST or None, initial=initial)
  
  if request.POST:
    if form.is_valid():
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password'])
      user.save()
      user.send_verify(get_current_site(request))
      
      user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
      login(request, user)
      
      messages.success(request, 'Sign up successful. Please check {} to verify your e-mail address.'.format(form.cleaned_data['email']))
      return http.HttpResponseRedirect(form.cleaned_data['redirect'])
      
  return TemplateResponse(request, 'profiles/signup.html', {'form': form, 'title': 'Sign Up'})
  
def logout_view (request):
  logout(request)
  return http.HttpResponseRedirect("/")
  
@ensure_csrf_cookie
def login_view (request):
  error = None
  
  form = LoginForm(request.POST or None, initial=request.GET or None)
  if request.POST:
    if form.is_valid():
      user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
      if user is not None:
        if user.is_active:
          login(request, user)
          return http.HttpResponseRedirect(form.cleaned_data['redirect'])
          
        else:
          error = "Your account has been deactivated."
          
      else:
        error = "Invalid Login"
        
  return TemplateResponse(request, 'profiles/login.html', {'form': form, 'title': 'Sign In', 'error': error})
  
@login_required
def profile (request):
  if request.POST:
    form = ProfileForm(request.POST, request.FILES, instance=request.user)
    formset = SocialHandleFormSet(request.POST, instance=request.user)
    
    if form.is_valid() and formset.is_valid():
      user = form.save()
      user.send_verify(get_current_site(request))
      formset.save()
      
      messages.success(request, 'Profile Updated!')
      if not user.verified_email or user.email.lower() != user.verified_email.lower():
        messages.success(request, 'Please check {} to verify your e-mail address.'.format(form.cleaned_data['email']))
        
      return http.HttpResponseRedirect("./")
      
  else:
    form = ProfileForm(instance=request.user)
    formset = SocialHandleFormSet(instance=request.user)
    
  return TemplateResponse(request, 'profiles/edit.html', {'form': form, 'title': 'My Profile', 'formset': formset})
  
def email_verify (request):
  secret = request.GET.get('secret', '')
  old = timezone.now() - datetime.timedelta(days=10)
  ev = get_object_or_404(EmailVerification, secret=secret, created__gte=old, used=False)
  ev.user.email = ev.sent_to
  ev.user.save()
  ev.used = True
  ev.save()
  
  return TemplateResponse(request, 'profiles/verification_success.html', {'title': "Verification Successful"})
  