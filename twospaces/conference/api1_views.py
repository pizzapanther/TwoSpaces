from bunch import Bunch

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from twospaces.conference.models import Session
from twospaces.conference.serializers import ProposedReadSizzler

@api_view(['GET'])
@permission_classes((AllowAny, ))
def proposed_talks (request):
  talks = []
  conf = request.GET.get('conf', '')
  
  for t in (
    ('talk-short', 'Short Talks'),
    ('talk-long', 'Long Talks'),
    ('talk-long', 'Long Talks'),
    ('tutorial', 'Tutorials'),
    ('lightning', 'Lightning Talks'),
  ):
    talks.append(
      [t[1], Session.objects.filter(stype=t[0], conference__slug=conf).exclude(status='declined').order_by('name')]
    )
    
  for i in range(0, len(talks)):
    talks[i][1] = ProposedReadSizzler(talks[i][1], many=True).data
    
  return Response(talks, status=200)
  