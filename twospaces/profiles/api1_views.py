from django.shortcuts import get_object_or_404
from django.db.models import Q

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
  
