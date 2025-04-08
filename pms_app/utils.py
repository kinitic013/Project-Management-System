from .models import ActivityLog , Project , Task , Images
from django.utils import timezone
from .serializers import ProjectSerializer ,  TaskSerializer , ImagesSerializer ,UserSerializer
from django.contrib.auth.models import User



def log_activity(user, action, changed_object,changed_object_id,ip_address=None,updated_field=[]):
    message = f"{user.username} performed '{action}' action on '{changed_object}' object with id {changed_object_id} at {timezone.now()}"
    if(action == "UPDATE" and updated_field != []):
        message += f" and updated field : { ', '.join(updated_field) }"
               
    ActivityLog.objects.create(
        user=user,
        action=action,
        changed_object=changed_object,
        message=message,
        ip_address=ip_address
    )
    
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
