from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="Your Project API",
      default_version='v1',
      description="API documentation for your project",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pms_app.urls')), 
    path('api-auth/', include('rest_framework.urls')),
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
