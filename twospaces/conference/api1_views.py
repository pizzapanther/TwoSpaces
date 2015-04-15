from bunch import Bunch

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from twospaces.conference.models import Session, Conference
from twospaces.conference.serializers import ProposedReadSizzler, SessionSizzler, ConferenceReadSizzler

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
  if request.user.phone and request.user.biography:
    pass
    
  else:
    return Response({'message': 'Fill out your speaker profile before submitting.'}, status=400)
    
  if request.JSON():
    conf = get_object_or_404(Conference, slug=request.JSON()['conf'])
    
  else:
    conf = get_object_or_404(Conference, slug=request.GET.get('conf', ''))
    
  if tid:
    session = get_object_or_404(Session, id=tid, user=request.user)
    
  else:
    now = timezone.now()
    if conf.cfp_open and conf.cfp_closed:
      if conf.cfp_open <= now and now <= conf.cfp_closed:
        pass
        
      else:
        return Response({'message': 'Talk submission is closed'}, status=400)
        
    else:
      return Response({'message': 'Talk submission is closed'}, status=400)
      
  if request.JSON():
    sizzle = SessionSizzler(session, data=request.JSON())
    if sizzle.is_valid():
      obj = sizzle.save(
        conference=conf,
        user=request.user,
      )
      obj.set_duration()
      obj.save()
      if tid is None:
        obj.send_submitted(request, conf)
        
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
  
@api_view(['GET'])
@permission_classes((AllowAny, ))
@ensure_csrf_cookie
def conf_data (request):
  conf = request.GET.get('conf', '')
  conf = get_object_or_404(Conference, slug=conf)
  
  return Response(ConferenceReadSizzler(conf).data, status=200)
  