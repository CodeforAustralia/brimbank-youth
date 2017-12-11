from django.db import models
from django.urls import reverse

from datetime import datetime

import arrow

#ACTIVITY_TYPE = (
#    ('Soccer', 'Soccer'),
#    ('Dance', 'Dance'),
#    ('Swimming', 'Swimming'),
#)

def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/image/{1}'.format(instance.name, filename)

# Create your models here.
class ActivityType(models.Model):
    name = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name
    
class Activity(models.Model):
    name = models.CharField(max_length=150)
#    activity_type = models.CharField(max_length=50, blank=True)
    activity_type = models.ForeignKey(ActivityType, related_name='activities', null=True)
    location = models.CharField(max_length=150, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    description = models.CharField(max_length=150, blank=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    start_time = models.TimeField(default=datetime.now, blank=True)
    end_time = models.TimeField(default=datetime.now, blank=True)
    activity_img = models.ImageField(upload_to=image_directory_path, blank=True)
#    time_zone = TimeZoneField(default='Australia/Melbourne')

    # Additional fields not visible to users
#    created_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
#        return 'Appointment #{0} - {1}'.format(self.pk, self.name)
        return self.name
    
#    def get_absolute_url(self):
#        return reverse('home')
    
#    def clean(self):
#        """Checks that appointments are not scheduled in the past"""
#        appointment_time = arrow.get(self.time, self.time_zone.zone)
#        if appointment_time < arrow.utcnow():
#            raise ValidationError('You cannot schedule an appointment for the past. Please check your time and time_zone')

class ActivityDraft(models.Model):
    name = models.CharField(max_length=150)
    activity_type = models.ForeignKey(ActivityType, related_name='activity_drafts', null=True)
    location = models.CharField(max_length=150, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    description = models.CharField(max_length=150, blank=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    start_time = models.TimeField(default=datetime.now, blank=True)
    end_time = models.TimeField(default=datetime.now, blank=True)
    activity_img = models.ImageField(upload_to=image_directory_path, blank=True)
    