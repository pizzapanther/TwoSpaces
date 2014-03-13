from .models import SponsorshipLevel

def sponsors (request):
  context = {}
  if hasattr(request, 'conference') and request.conference:
    context['sponsorLevels'] = SponsorshipLevel.objects.filter(conference__id=request.conference['id'])
    
  return context