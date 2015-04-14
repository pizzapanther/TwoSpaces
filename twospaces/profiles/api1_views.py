from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from twospaces.profiles.models import User
from twospaces.profiles.serializers import UserPublicSizzler

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
    response = Response({'status': 'OK'}, status=200)
    response.set_cookie('angular_logged_in', value='true', httponly=False)
    return response
    
  return Response({'errors': {'username': ['Username or Password is incorrect.']}}, status=400)
  
@api_view(['POST'])
@permission_classes((AllowAny, ))
def logout_view (request):
  logout(request)
  response = Response({'status': 'OK'}, status=200)
  response.delete_cookie('angular_logged_in')
  return response
  
@api_view(['GET'])
@permission_classes((AllowAny, ))
@ensure_csrf_cookie
def csrf_generator (request):
  return Response({'status': 'OK'}, status=200)
  