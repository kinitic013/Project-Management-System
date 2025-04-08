import os
import csv
from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
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
    ActivityLogSerializer
)
from ..utils import log_activity, get_client_ip
from ..constants import ActivityActions, ModelActions

@api_view(['POST'])
def signup(request):
    email = request.data.get('email')
    password = request.data.get('password')
    username =  request.data.get('username')
    client_ip = get_client_ip(request)

    if email and password and username:
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            log_activity(user, ActivityActions.CREATE, ModelActions.USER, user.id,client_ip,[])
            return JsonResponse({"message": "Account Created successfully"} , status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return JsonResponse({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)