from django.db import models

# Create your models here.
class Event(models.Model):
    description = models.TextField(max_length=4000, null=True)
    organizer = models.CharField(max_length=255, null=True)
    building = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=30, null=True)
    postcode = models.CharField(max_length=20, null=True)
    event_id = models.CharField(max_length=20, null=True)
    page_id = models.CharField(max_length=255, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.event_id