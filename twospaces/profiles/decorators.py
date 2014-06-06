import urllib

from django import http
from django.core.urlresolvers import reverse

def login_required (target):
  def wrapper (*args, **kwargs):
    if args[0].user.is_authenticated() and args[0].user.is_active:
      return target(*args, **kwargs)
      
    redirect = urllib.quote(args[0].get_full_path())
    return http.HttpResponseRedirect(reverse("profiles:login") + '?redirect=' + redirect)
    
  return wrapper
  
def speaker_info_required (target):
  def wrapper (*args, **kwargs):
    user = args[0].user
    if user.biography and user.phone and user.first_name and user.last_name:
      return target(*args, **kwargs)
      
    redirect = urllib.quote(args[0].get_full_path())
    return http.HttpResponseRedirect(reverse("profiles:speaker-info") + '?redirect=' + redirect)
    
  return wrapper
  