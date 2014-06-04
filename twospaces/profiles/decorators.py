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
  