from django.db import models
from django.contrib.auth.models import User

# Options
GENDER = (  
    ('F', 'Female'),
    ('M', 'Male'),
)

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True)

    def __str__(self):
        return self.user.username