import os
import csv
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ..models import Project, Task, Images, ActivityLog
from ..serializers import (
    ProjectSerializer,
    TaskSerializer,
    ImagesSerializer,
    UserSerializer,
    ActivityLogSerializer,
    SignupSerializer
)
from ..utils import log_activity, get_client_ip
from ..constants import ActivityActions, ModelActions

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(method='post', request_body=SignupSerializer)
@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if(serializer.is_valid()):
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            client_ip = get_client_ip(request)
            log_activity(user, ActivityActions.CREATE, ModelActions.USER, user.id, client_ip, [])
            return JsonResponse({"message": "Account created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)