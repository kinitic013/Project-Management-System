from django.urls import path
from .views import (
    project_views,
    task_views,
    image_views,
    activity_views,
    auth_views
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    # Auth
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', auth_views.signup, name='signup'),

    # Projects
    path('projects/create', project_views.create_project, name='create_project'),
    path('projects/get_filter', project_views.get_projects_by_user, name='get_projects_by_user'),
    path('projects/get', project_views.get_all_projects_by_user, name='get_all_projects_by_user'),
    path('projects/<int:project_id>/update', project_views.update_project, name='update_project'),
    path('projects/<int:project_id>/soft_delete', project_views.soft_delete, name='soft_delete'),

    # Export CSV
    path('projects/<int:project_id>/get_csv', project_views.get_project_csv, name='get_project_csv'),

    # Tasks
    path('projects/<int:project_id>/tasks/create', task_views.create_task, name='create_task'),
    path('projects/<int:project_id>/tasks/get_all', task_views.get_tasks_by_project, name='get_tasks_by_project'),
    path('projects/<int:project_id>/tasks/<int:task_id>/get', task_views.get_task_by_id, name='get_task_by_id'),
    path('projects/<int:project_id>/tasks/<int:task_id>/update_status', task_views.update_task_status, name='update_task_status'),
    path('projects/<int:project_id>/tasks/<int:task_id>/delete', task_views.delete_task, name='delete_task'),

    # Images
    path('projects/<int:project_id>/images/upload', image_views.upload_image, name='upload_image'),
    path('projects/<int:project_id>/images/get_all', image_views.get_all_images_project, name='get_all_images_project'),
    path('projects/<int:project_id>/images/<int:image_id>/get', image_views.get_image_by_id, name='get_images_by_project'),

    # User activity
    path('user/get_all_activity', activity_views.get_all_activity_records, name='get_all_activity_records'),
]
