import datetime

from django import http
from django import forms
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from twospaces.profiles.models import User, EmailVerification
from twospaces.profiles.serializers import UserPublicSizzler, UserSizzler, UserUpdateSizzler

from django_gravatar.helpers import get_gravatar_url

@api_view(['GET'])
@permission_classes((AllowAny, ))
def user_detail (request, username):
  queryset = get_object_or_404(User, ~Q(is_active=False), username=username)
  return Response(UserPublicSizzler(queryset).data, status=200)
  
@api_view(['POST'])
@permission_classes((AllowAny, ))
def login_view (request):
  json_data = request.JSON()
  
  user = authenticate(
    username=json_data.get('username'),
    password=json_data.get('password')
  )
  
  if user:
    login(request, user)
    
    value = 'user'
    if user.phone and user.biography:
      value = 'speaker'
      
    response = Response({'status': 'OK'}, status=200)
    response.set_cookie('angular_logged_in', value=value, httponly=False)
    return response
    
  return Response({'errors': {'username': ['Username or Password is incorrect.']}}, status=400)
  
@api_view(['POST'])
@permission_classes((AllowAny, ))
def logout_view (request):
  logout(request)
  response = Response({'status': 'OK'}, status=200)
  response.delete_cookie('angular_logged_in')
  return response
  
@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, ))
def profile_image (request):
  if request.JSON():
    if request.JSON().get('gravatar', ''):
      request.user.avatar = None
      request.user.save()
      
  images = {
    'gravatar': get_gravatar_url(request.user.email, size=256)
  }
  
  if request.user.avatar:
    images['image'] = request.user.avatar.url
    
  return Response(images, status=200)
  
class AvatarForm (forms.ModelForm):
  avatar = forms.ImageField(required=True)
  
  class Meta:
    model = User
    fields = ['avatar']
    
def avatar_upload (request):
  url = request.POST.get('ret', '/')
  
  if 'avatar' in request.FILES:
    form = AvatarForm(request.POST, request.FILES, instance=request.user)
    
    if form.is_valid():
      form.save()
      return http.HttpResponseRedirect('{}?success=1'.format(url))
      
  return http.HttpResponseRedirect('{}?error=1'.format(url))
  
@api_view(['POST', 'GET'])
@permission_classes((AllowAny, ))
def edit_profile (request):
  user = None
  Sizzler = UserSizzler
  json_data = request.JSON()
  
  if request.user.is_authenticated():
    user = request.user
    Sizzler = UserUpdateSizzler
    
  if json_data:
    sizzle = Sizzler(user, data=json_data)
    if sizzle.is_valid():
      obj = sizzle.save()
      
      if user is None:
        obj.set_password(sizzle.validated_data['password'])
        obj.save()
        
        obj = authenticate(
          username=sizzle.validated_data['username'],
          password=sizzle.validated_data['password']
        )
        login(request, obj)
        
      else:
        if 'password' in sizzle.validated_data:
          obj.set_password(sizzle.validated_data['password'])
          obj.save()
          update_session_auth_hash(request, obj)
          
      value = 'user'
      if obj.phone and obj.biography:
        value = 'speaker'
        
      obj.send_verify(request, json_data['conf'])
      response = Response({'status': 'OK'}, status=200)
      response.set_cookie('angular_logged_in', value=value, httponly=False)
      return response
      
    else:
      return Response({'errors': sizzle.errors}, status=400)
      
  else:
    sizzle = Sizzler(user)
    
  return Response(sizzle.data, status=200)
  
@api_view(['POST'])
@permission_classes((AllowAny, ))
def verify (request):
  json_data = request.JSON()
  if json_data:
    secret = json_data.get('secret', '')
    if secret:
      old = timezone.now() - datetime.timedelta(days=10)
      ev = get_object_or_404(EmailVerification, secret=secret, created__gte=old, used=False)
      ev.user.verified_email = ev.sent_to
      ev.user.save()
      ev.used = True
      ev.save()
      return Response({'status': 'OK'}, status=200)
      
  return Response({'status': 'invalid'}, status=400)
  
@api_view(['POST'])
@permission_classes((AllowAny, ))
def start_reset_password (request):
  json_data = request.JSON()
  if json_data:
    user = None
    try:
      if 'username' in json_data and json_data['username']:
        user = User.objects.get(username=json_data['username'])
        
      elif 'email' in json_data and json_data['email']:
        user = User.objects.get(email=json_data['email'])
        
    except User.DoesNotExist:
      return Response({'message': 'Can not find record.'}, status=400)
      
    if user:
      user.send_reset(request, json_data['conf'])
      return Response({'status': 'OK'}, status=200)
      
  return Response({'message': 'No data provided'}, status=400)
  
@api_view(['POST'])
@permission_classes((AllowAny, ))
def finish_reset_password (request):
  json_data = request.JSON()
  if json_data:
    if 'secret' in json_data:
      old = timezone.now() - datetime.timedelta(days=10)
      try:
        ev = EmailVerification.objects.get(secret=json_data['secret'], created__gte=old, used=False)
        
      except EmailVerification.DoesNotExist:
        return Response({'message': 'Invalid reset key.'}, status=400)
        
      else:
        if 'password' in json_data:
          ev.user.verified_email = ev.sent_to
          ev.user.set_password(json_data['password'])
          ev.user.save()
          
          ev.used = True
          ev.save()
          
        return Response({'status': 'OK'}, status=200)
        
  return Response({'message': 'No data provided'}, status=400)
  