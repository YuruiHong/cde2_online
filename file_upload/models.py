from django.db import models
import os
import uuid

# Create your models here.
# Define user directory path


def user_directory_path(instance, filename):
    while True:
        dir_name = uuid.uuid4().hex[:10]
        return os.path.join("files", dir_name, filename)


class File(models.Model):
    file = models.FileField(upload_to=user_directory_path, null=True)
    description = models.CharField(max_length=40, null=True)
    attributes = models.CharField(max_length=200, null=True)
    contributor = models.CharField(max_length=20)
    uploaded_at = models.DateTimeField(auto_now_add=True)
