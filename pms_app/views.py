
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer ,  TaskSerializer , ImagesSerializer ,UserSerializer
from django.contrib.auth.models import User
from .models import Project, Task, Images


@api_view(['POST'])
def signup(request):
    email = request.data.get('email')
    password = request.data.get('password')
    username =  request.data.get('username')

    print(email,password,username)
    if email and password and username:
        try:
            User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({"message": "Login successful"})
        except Exception as e:
            print(e)
            return JsonResponse({"message": "User already exists"}, status=400)
    else:
        return JsonResponse({"message": "Invalid credentials"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_projects_by_user(request):
    user = request.user
    user = request.user  
    projects = user.projects.all() 
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)





@api_view(['POST'])
def create_project(request):
    name = request.data.get('name')
    description = request.data.get('description')
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    created_by = request.user
    if not all([name, description, start_date, end_date]):
        return JsonResponse({"message": "All fields are required"}, status=400)
    try:
        project = Project.objects.create(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            created_by=created_by
        )
        return JsonResponse({"message": "Project created successfully"}, status=201)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Error occurred"}, status=400)

    

