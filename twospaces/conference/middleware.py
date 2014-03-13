from django.core.cache import get_cache

cache = get_cache('default')

from .models import get_set_conferences

class ConferenceMiddleware (object):
  def process_request (self, request):
    slug = None
    conferences = get_set_conferences()
    request.default_conference = None
    for conf in conferences:
      if conf['default']:
        request.default_conference = conf
        break
        
    request.conference = request.default_conference
    
    if slug:
      for conf in conferences:
        if conf['slug'] == slug:
          request.conference = conf
          break
          