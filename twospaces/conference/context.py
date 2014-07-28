from django.conf import settings

from .models import SponsorshipLevel, Sponsor

def sponsors (request):
  context = {}
  context['STRIPE_PUB_KEY'] = getattr(settings, 'STRIPE_PUB_KEY', '')
  
  if hasattr(request, 'conference') and request.conference:
    context['sponsorLevels'] = SponsorshipLevel.objects.filter(conference__id=request.conference['id'])
    
  context['sponsorCount'] = Sponsor.objects.filter(
    level__conference__id=request.conference['id'], active=True
  ).count()
  
  return context