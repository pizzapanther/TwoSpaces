from bunch import Bunch

from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from twospaces.conference.models import Session, Conference
from twospaces.conference.serializers import ProposedReadSizzler, SessionSizzler

@api_view(['GET'])
@permission_classes((AllowAny, ))
def proposed_talks (request):
  talks = []
  conf = request.GET.get('conf', '')
  
  for t in (
    ('talk-short', 'Short Talks'),
    ('talk-long', 'Long Talks'),
    ('tutorial', 'Tutorials'),
    ('lightning', 'Lightning Talks'),
  ):
    talks.append(
      [t[1], Session.objects.filter(stype=t[0], conference__slug=conf).exclude(status='declined').order_by('name')]
    )
    
  for i in range(0, len(talks)):
    talks[i][1] = ProposedReadSizzler(talks[i][1], many=True, exclude=['description']).data
    
  return Response(talks, status=200)
  
@api_view(['GET'])
@permission_classes((AllowAny, ))
def talk_detail (request, tid):
  conf = request.GET.get('conf', '')
  queryset = get_object_or_404(
    Session, ~Q(status='declined'), id=tid, conference__slug=conf)
  
  return Response(ProposedReadSizzler(queryset).data, status=200)
  
@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, ))
def edit_talk (request, tid=None):
  session = None
  if tid:
    session = get_object_or_404(Session, id=tid, user=request.user)
    
  if request.JSON():
    sizzle = SessionSizzler(session, data=request.JSON())
    if sizzle.is_valid():
      conf = get_object_or_404(Conference, slug=request.JSON()['conf'])
      
      obj = sizzle.save(
        conference=conf,
        user=request.user,
      )
      obj.set_duration()
      obj.save()
      if tid is None:
        obj.send_submitted(request)
        
      return Response({'status': 'OK'}, status=200)
      
    else:
      return Response({'errors': sizzle.errors}, status=400)
      
  else:
    sizzle = SessionSizzler(session)
    
  return Response(sizzle.data, status=200)
  
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def my_talks (request):
  conf = request.GET.get('conf', '')
  queryset = Session.objects.filter(conference__slug=conf, user=request.user).order_by('name')
  talks = ProposedReadSizzler(queryset, many=True, exclude=['description', 'user']).data
  return Response(talks, status=200)
  