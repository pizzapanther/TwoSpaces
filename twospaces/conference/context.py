from django.conf import settings

from .models import SponsorshipLevel

def sponsors (request):
  context = {}
  context['STRIPE_PUB_KEY'] = getattr(settings, 'STRIPE_PUB_KEY', '')
  
  if hasattr(request, 'conference') and request.conference:
    context['sponsorLevels'] = SponsorshipLevel.objects.filter(conference__id=request.conference['id'])
    
  return context