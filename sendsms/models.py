from django.db import models
from django.utils.timezone import now

# Create your models here.
class SendSMS(models.Model):
    recipient_no = models.CharField(max_length=50, blank=True)
    message = models.CharField(max_length=500, blank=True)
    sent_time = models.DateTimeField(default = now)
    
    def __str__(self):
        return str(self.recipient_no+sent_time)
    
class SendEmail(models.Model):
    email = models.EmailField(blank=True)
    message = models.TextField(max_length=500, blank=True)
    sent_time = models.DateTimeField(default = now)
    
    def __str__(self):
        return str(self.email+sent_time)