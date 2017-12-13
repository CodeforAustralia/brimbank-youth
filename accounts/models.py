from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Options
GENDER = (  
    ('F', 'Female'),
    ('M', 'Male'),
)

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)
    organisation_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()