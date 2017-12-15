from django.db import models
from django.urls import reverse

from datetime import datetime

import arrow

TERMS = (
    ('Once', 'Only once'),
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Fortnightly', 'Fortnightly'),
    ('Monthly', 'Monthly'),
)

DAYS_CHOICE = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)

LIVING_DURATION = (
    ('Less', 'Less than 5 years'),
    ('More', 'More than 5 years'),
    ('Open', 'Open'),
)

GENDER = (
    ('F', 'Only females'),
    ('M', 'Only males'),
    ('B', 'Both'),
)

ACTIVITY_TYPES = (
    ('Sports', 'Sports'),
    ('Fun', 'Fun'),
    ('Learn', 'Learn'),
    ('Job', 'Get a job'),
    ('Culture', 'Culture'),
)

LISTING_PRIVACY = (
    ('Public', 'Public Page: Accessible by anyone on Youthposter'),
    ('Private', 'Private Page: Accesible by only people you specify'),
)

def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/image/{1}'.format(instance.name, filename)

def file_directory_path(instance, filename):
    return '{0}/flyer/{1}'.format(instance.name, filename)

# Create your models here.
class ActivityType(models.Model):
    name = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name
    
class Activity(models.Model):
    name = models.CharField(max_length=150)
    activity_type = models.CharField(max_length=100, choices=ACTIVITY_TYPES, blank=True, default='Sports')
    term = models.CharField(max_length=50, choices=TERMS, blank=True, default='Once')
    location = models.CharField(max_length=150, blank=True, null=True)
    organiser = models.CharField(max_length=150, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    description = models.TextField(max_length=150, blank=True, null=True)
    activity_date = models.DateField(blank=True, null=True) # for one-time activity
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    activity_day = models.CharField(max_length=50, choices=DAYS_CHOICE, blank=True, default='Monday')
    start_time = models.TimeField(default=datetime.now, blank=True, null=True)
    end_time = models.TimeField(default=datetime.now, blank=True, null=True)
    activity_img = models.ImageField(upload_to=image_directory_path, blank=True, null=True)
    flyer = models.FileField(upload_to=file_directory_path, blank=True, null=True)
    min_age = models.PositiveSmallIntegerField(blank=True, null=True)
    max_age = models.PositiveSmallIntegerField(blank=True, null=True)
    background = models.CharField(max_length=150, blank=True, null=True)
    living_duration = models.CharField(max_length=50, choices=LIVING_DURATION, blank=True, default='Less')
    gender = models.CharField(max_length=50, choices=GENDER, blank=True, default='F')
    cost = models.FloatField(blank=True, null=True)
    space = models.PositiveSmallIntegerField(blank=True, null=True, default=10000)
    listing_privacy = models.CharField(max_length=50, choices=LISTING_PRIVACY, blank=True, default='Public')
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
#    activity_type = models.ForeignKey(ActivityType, related_name='activity_drafts', null=True)
    activity_type = models.CharField(max_length=100, choices=ACTIVITY_TYPES, blank=True, default='Sports')
    term = models.CharField(max_length=50, choices=TERMS, blank=True, default='Once')
    location = models.CharField(max_length=150, blank=True, null=True)
    organiser = models.CharField(max_length=150, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    description = models.TextField(max_length=150, blank=True, null=True)
    activity_date = models.DateField(blank=True, null=True) # for one-time activity
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    activity_day = models.CharField(max_length=50, choices=DAYS_CHOICE, blank=True, default='Monday')
    start_time = models.TimeField(default=datetime.now, blank=True, null=True)
    end_time = models.TimeField(default=datetime.now, blank=True, null=True)
    activity_img = models.ImageField(upload_to=image_directory_path, blank=True, null=True)
    flyer = models.FileField(upload_to=file_directory_path, blank=True, null=True)
    min_age = models.PositiveSmallIntegerField(blank=True, null=True)
    max_age = models.PositiveSmallIntegerField(blank=True, null=True)
    background = models.CharField(max_length=150, blank=True, null=True)
    living_duration = models.CharField(max_length=50, choices=LIVING_DURATION, blank=True, default='Less')
    gender = models.CharField(max_length=50, choices=GENDER, blank=True, default='F')
    cost = models.FloatField(blank=True, null=True)
    space = models.PositiveSmallIntegerField(blank=True, null=True, default=10000)
    listing_privacy = models.CharField(max_length=50, choices=LISTING_PRIVACY, blank=True, default='Public')
    
    def __str__(self):
        return self.name
    