# Generated by Django 5.2 on 2025-04-08 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pms_app', '0002_remove_project_is_deleted_project_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_deleted',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
