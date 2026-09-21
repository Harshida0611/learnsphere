# models.py

from django.db import models

class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField()
    password = models.CharField(max_length=128)
    technology = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
