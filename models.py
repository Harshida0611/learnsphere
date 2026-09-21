from django.db import models
from django.contrib.auth.models import User

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    pdf_file = models.FileField(upload_to="assignments/", blank=True, null=True)


    
