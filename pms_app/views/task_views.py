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
@permission_classes([IsAuthenticated])
def create_task(request , project_id):
    client_ip = get_client_ip(request)
    user = request.user
    if(project_id == None):
        return Response({"message": "Project ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    if('name' not in request.data):
        return Response({"message": "Task name is required"}, status=status.HTTP_400_BAD_REQUEST)

    name = request.data.get('name')
    try:
        project = Project.objects.get(id=project_id, created_by=user , is_deleted=False)
    except Project.DoesNotExist:
        return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"message": "Error occurred"}, status=status.HTTP_400_BAD_REQUEST)

    newTask = Task.objects.create(
        project=project,
        name=name,
    )
    try:
        newTask.save()
        serializer = TaskSerializer(newTask)
        log_activity(user, ActivityActions.CREATE, ModelActions.TASK , user.id,client_ip,[])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response({"message": "Error occurred"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks_by_project(request,project_id):
    client_ip = get_client_ip(request)
    user = request.user
    if(project_id == None):
        return Response({"message": "Project ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    try: 
        status_filter = request.GET.get('status')
        project = Project.objects.filter(id=project_id, created_by=user)
        allTask = project[0].tasks.all()

        if status_filter:
            allTask = allTask.filter(status=status_filter)
        serializer = TaskSerializer(allTask, many=True)
        log_activity(user, ActivityActions.GET, ModelActions.TASK , user.id,client_ip,[])
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"message": "Error occurred"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_by_id(request,project_id,task_id):
    client_ip = get_client_ip(request)
    user = request.user
    if(project_id == None):
        return Response({"message": "Project ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    if(task_id == None):
        return Response({"message": "Task ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        task = Task.objects.get(id=task_id, project__id=project_id, project__created_by=user)
        serializer = TaskSerializer(task)
        log_activity(user, ActivityActions.GET, ModelActions.TASK , user.id,client_ip,[])
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"message": "Error occurred"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_task_status(request,project_id,task_id):
    client_ip = get_client_ip(request)
    user = request.user
    if(project_id == None):
        return Response({"message": "Project ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    if(task_id == None):
        return Response({"message": "Task ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    if('status' not in request.data):
        return Response({"message": "Task status is required"}, status=status.HTTP_400_BAD_REQUEST)
    new_status = request.data.get('status')
    if(new_status not in ['Pending', 'Completed']):
        return Response({"message": "Invalid status value. Use 'Pending' or 'Completed'"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        task = Task.objects.get(id=task_id, project__id=project_id, project__created_by=user)
        task.status = new_status
        task.save()
        log_activity(user, ActivityActions.UPDATE, ModelActions.TASK , user.id,client_ip,['status'])
        return Response({"message": "Task status updated successfully"}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"message": "Error occurred"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request,project_id,task_id):
    client_ip = get_client_ip(request)
    user = request.user
    if(project_id == None):
        return Response({"message": "Project ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    if(task_id == None):
        return Response({"message": "Task ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        task = Task.objects.get(id=task_id, project__id=project_id, project__created_by=user)
        task.delete()
        log_activity(user, ActivityActions.DELETE, ModelActions.TASK , user.id,client_ip,[])
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"message": "Error occurred"}, status=status.HTTP_400_BAD_REQUEST)