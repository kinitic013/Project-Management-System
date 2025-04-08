
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer ,  TaskSerializer , ImagesSerializer ,UserSerializer
from django.contrib.auth.models import User
from .models import Project, Task, Images
from datetime import datetime
from rest_framework import status
from django.core.paginator import Paginator


@api_view(['POST'])
def signup(request):
    email = request.data.get('email')
    password = request.data.get('password')
    username =  request.data.get('username')

    print(email,password,username)
    if email and password and username:
        try:
            User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({"message": "Login successful"} , status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return JsonResponse({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_projects_by_user(request):
    user = request.user
    try : 
        projects = user.projects.all() 
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error occurred"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_projects_by_user(request):
    user = request.user

    name_filter = request.GET.get('name', '')
    start_date_filter = request.GET.get('start_date', '')
    end_date_filter = request.GET.get('end_date', '')

    page_number = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 5))

    projects = user.projects.filter(is_deleted=False)

    if name_filter:
        projects = projects.filter(name__icontains=name_filter)
    
    if start_date_filter:
        try:
            start_date = datetime.strptime(start_date_filter, "%d-%m-%Y").date()
            projects = projects.filter(start_date__gte=start_date)
        except ValueError:
            return Response({"message": "Invalid start date format. Use DD-MM-YYYY"}, status=status.HTTP_400_BAD_REQUEST)
    
    if end_date_filter:
        try:
            end_date = datetime.strptime(end_date_filter, "%d-%m-%Y").date()
            projects = projects.filter(end_date__lte=end_date)
        except ValueError:
            return Response({"message": "Invalid end date format. Use DD-MM-YYYY"}, status=status.HTTP_400_BAD_REQUEST)

    
    paginator = Paginator(projects, page_size)
    
    try:
        page_obj = paginator.page(page_number)
    except:
        return Response({"message": "Invalid page number"}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = ProjectSerializer(page_obj, many=True, context={'request': request})

    pagination_data = {
        "total_items": paginator.count,
        "total_pages": paginator.num_pages,
        "current_page": page_number,
        "page_size": page_size,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
    }
    
    return Response({
        "results": serializer.data,
        "pagination": pagination_data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project(request):
    name = request.data.get('name')
    description = request.data.get('description')
    start_date_str = request.data.get('start_date') 
    end_date_str = request.data.get('end_date')
    try : 
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y").date()
    except  ValueError:
        return JsonResponse({"message": "Invalid start date format. Use DD-MM-YYYY"}, status=status.HTTP_400_BAD_REQUEST)
    try :   
        end_date = datetime.strptime(end_date_str, "%d-%m-%Y").date()
    except ValueError:  
        return JsonResponse({"message": "Invalid end date format. Use DD-MM-YYYY"}, status=status.HTTP_400_BAD_REQUEST)
    if start_date > end_date:
        return JsonResponse({"message": "Start date must be before end date"}, status=status.HTTP_400_BAD_REQUEST)

    created_by = request.user
    if not all([name, description, start_date, end_date]):
        return JsonResponse({"message": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        project = Project.objects.create(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            created_by=created_by
        )
        return JsonResponse({"message": "Project created successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error occurred"}, status=status.HTTP_400_BAD_REQUEST)

    

