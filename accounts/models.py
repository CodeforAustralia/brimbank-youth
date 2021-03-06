from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Options
GENDER = (  
    ('F', 'Female'),
    ('M', 'Male'),
)

def image_directory_path(instance, filename):
    return '{0}/image/{1}'.format(instance.name, filename)

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)
    organisation_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=300, blank=True)
    role = models.CharField(max_length=100, blank=True)
    staff_name = models.CharField(max_length=50, blank=True)
    web_address = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    sms_limit = models.PositiveSmallIntegerField(default=30)
    email_limit = models.PositiveSmallIntegerField(default=30)
    recharged = models.BooleanField(default=True)
    last_recharged = models.DateField(auto_now_add=True, null=True)
    # organisation_logo = models.ImageField(upload_to=image_directory_path, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class ModifyValue(models.Model): 
    sms_limit = models.PositiveSmallIntegerField(default=30)
    email_limit = models.PositiveSmallIntegerField(default=30)
    admin_email = models.EmailField(blank=True)

class AdminEmail(models.Model): 
    role = models.CharField(max_length=100, default='admin')
    email = models.EmailField(blank=True, default='devys@brimbank.vic.gov.au')

    def __str__(self):
        return self.email