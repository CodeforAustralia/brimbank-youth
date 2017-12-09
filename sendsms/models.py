from django.db import models

# Create your models here.
class SendSMS(models.Model):
    recipient_no = models.CharField(max_length=50, blank=True)
    message = models.CharField(max_length=500, blank=True)
    
    def __str__(self):
        return self.recipient_no