import datetime

from bunch import Bunch

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.cache import cache_page
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from twospaces.conference.models import Session, Conference, SponsorshipLevel
from twospaces.conference.serializers import ProposedReadSizzler, \
  SessionSizzler, ConferenceReadSizzler, SponsorshipLevelSizzler, \
  SessionScheduleSizzler

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
  
@api_view(['GET'])
@permission_classes((AllowAny, ))
def sponsor_data (request):
  conf = request.GET.get('conf', '')
  conf = get_object_or_404(Conference, slug=conf)
  queryset = SponsorshipLevel.objects.filter(conference=conf)
  return Response(SponsorshipLevelSizzler(queryset, many=True).data, status=200)
  
def append_room (hour, room_key, talk):
  if room_key not in hour:
    hour[room_key] = {'talks': [talk]}
    
  else:
    hour[room_key]['talks'].append(talk)
    
@api_view(['GET'])
@permission_classes((AllowAny, ))
@cache_page(settings.API_CACHE)
def schedule (request):
  schedule = []
  conf = request.GET.get('conf', '')
  conf = get_object_or_404(Conference, slug=conf)
  
  d = conf.start
  while d <= conf.end:
    queryset = Session.objects.filter(
      status='accepted',
      conference=conf,
      start__month=d.month,
      start__day=d.day,
      start__year=d.year,
    ).exclude(
      stype='lightning'
    ).order_by('start', 'room__sorder').select_related('room')
    sizzler = SessionScheduleSizzler(queryset, many=True)
    
    hours = []
    hour = {}
    last_hour = ''
    for i, talk in enumerate(sizzler.data):
      room_key = 'all'
      if talk['room'] and not talk['all_rooms']:
        room_key = talk['room']['name']
        
      h = talk['start'].split('T')[1].split(':')[0]
      if h != last_hour and i != 0:
        if talk['start'] == last_hour:
          append_room(hour, room_key, talk)
          
        else:
          hours.append(hour)
          hour = {}
          append_room(hour, room_key, talk)
          last_hour = h
          
      else:
        append_room(hour, room_key, talk)
        
    if len(hour.keys()) != 0:
      hours.append(hour)
      
    rooms = []
    for talk in queryset:
      if talk.room and talk.room.name not in rooms:
        rooms.append(talk.room.name)
        
    label = d.strftime("%a %d")
    if label.endswith('1'):
      label += 'st'
      
    elif label.endswith('2'):
      label += 'nd'
      
    elif label.endswith('3'):
      label += 'rd'
      
    else:
      label += 'th'
      
    s = {
      'year': d.year,
      'month': d.month,
      'day': d.day,
      'label': label,
      'hours': hours,
      'rooms': rooms,
    }
    
    schedule.append(s)
    d += datetime.timedelta(days=1)
    
  return Response(schedule, status=200)
  