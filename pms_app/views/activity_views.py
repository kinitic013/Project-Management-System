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

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='get',
    operation_summary="Get all activity logs",
    operation_description="Returns a list of all activity logs in the system. Requires authentication, paste access token you get in response of login with 'Bearer ' prefix. ",
    responses={200: ActivityLogSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_activity_records(request):
    client_ip = get_client_ip(request)
    user = request.user
    activity_logs = ActivityLog.objects.all()
    serializer = ActivityLogSerializer(activity_logs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)