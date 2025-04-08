from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('signup/', signup, name='signup'),
    path('projects/get_filter', get_projects_by_user, name='get_projects_by_user'),
    path('projects/get', get_all_projects_by_user, name='get_all_projects_by_user'),
    path('projects/create', create_project, name='create_project'),
    path('projects/<int:project_id>/update', update_project, name='update_project'),
    path('projects/<int:project_id>/soft_delete', soft_delete, name='soft_delete'),

    path('projects/<int:project_id>/tasks/create', create_task, name='create_task'),
    path('projects/<int:project_id>/tasks/get_all', get_tasks_by_project, name='get_tasks_by_project'),
    path('projects/<int:project_id>/tasks/<int:task_id>/get', get_task_by_id, name='get_task_by_id'),
    path('projects/<int:project_id>/tasks/<int:task_id>/update_status', update_task_status, name='update_task_status'),
    path('projects/<int:project_id>/tasks/<int:task_id>/delete', delete_task, name='delete_task'),
    # path('projects/<int:project_id>/images/upload', upload_image, name='upload_image'),
    # path('projects/<int:project_id>/images/get', get_images_by_project, name='get_images_by_project'),
]
