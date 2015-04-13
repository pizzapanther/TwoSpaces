import json

from rest_framework.response import Response

class ParseJSON (object):
  def __init__ (self, request):
    self.request = request
    self.cache = None
    
  def __call__ (self):
    if self.cache is None:
      if self.request.body:
        try:
          self.cache = json.loads(self.request.body.decode("utf-8"))
          
        except:
          self.cache = Response({'error-code': 'malformed'}, status=400)
          
      else:
        self.cache = {}
        
    return self.cache
    
class JsonRequest (object):
  def process_request (self, request):
    request.JSON = ParseJSON(request)
    