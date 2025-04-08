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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request,project_id):
    user = request.user
    client_ip = get_client_ip(request)
    if(project_id == None):
        return Response({"message": "Project ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        project = Project.objects.get(id=project_id, created_by=user , is_deleted=False)
    except Project.DoesNotExist:
        return Response({"message": "Project not found or access denied"}, status=status.HTTP_404_NOT_FOUND)
    
    if 'image' in request.FILES:
        image_file = request.FILES['image']
        filename = default_storage.get_available_name(image_file.name)
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        image = Images.objects.create(
            project=project,
            image=image_file
        )
        image.save()    
        serializer = ImagesSerializer(image)
        log_activity(user, ActivityActions.CREATE, ModelActions.IMAGE , user.id,client_ip,[])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:   
        return Response({"message": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST)
    

@swagger_auto_schema(
    method='get',
    responses={200: ImagesSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_images_project(request,project_id):
    client_ip = get_client_ip(request)
    user = request.user
    if(project_id == None):
        return Response({"message": "Project ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        project = Project.objects.get(id=project_id, created_by=user , is_deleted=False)
        images = project.images.all()
        serializer = ImagesSerializer(images, many=True)
        log_activity(user, ActivityActions.GET_ALL, ModelActions.IMAGE , user.id,client_ip,[])
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"message": "Error occurred"}, status=status.HTTP_400_BAD_REQUEST)
    
    
@swagger_auto_schema(
    method='get',
    responses={200: ImagesSerializer()}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_image_by_id(request,project_id,image_id):
    client_ip = get_client_ip(request)
    user = request.user
    if(project_id == None):
        return Response({"message": "Project ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        project = Project.objects.get(id=project_id, created_by=user , is_deleted=False)
        image = Images.objects.get(id=image_id, project=project)
        serializer = ImagesSerializer(image)
        log_activity(user, ActivityActions.GET, ModelActions.IMAGE , user.id,client_ip,[])
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"message": "Error occurred"}, status=status.HTTP_400_BAD_REQUEST)