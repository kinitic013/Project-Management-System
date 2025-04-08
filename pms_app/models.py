from django.db import models
from django.contrib.auth.models import User
from .constants import ActivityActions , ModelActions
class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.IntegerField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects',null =True)
    is_deleted = models.BooleanField(default=False , null=True)

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.duration = (self.end_date - self.start_date).days
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
]

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    def __str__(self):
        return self.name

class Images(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/')

    def __str__(self):
        return f"Image for {self.project.name}"
class ActivityLog(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=50, choices=ActivityActions.CHOICES)
    changed_object = models.CharField(max_length=255 , choices= ModelActions.CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.action} on {self.timestamp}"