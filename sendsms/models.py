from django.db import models
from django.utils.timezone import now

from contacts.models import ContactGroup, EmailGroup

# Create your models here.
class SendSMS(models.Model):
    recipient_no = models.CharField(max_length=50, blank=True, default='')
    recipient_group = models.ForeignKey(ContactGroup, related_name='sent_sms', null=True, blank=True)
    message = models.CharField(max_length=500, blank=True)
    activity_list = models.CharField(max_length=500, blank=True)
    sent_time = models.DateTimeField(default = now)
    
    def __str__(self):
        return str(self.message)
    
class SendEmail(models.Model):
    # recipients = models.EmailField(blank=True)
    recipients = models.CharField(max_length=500, blank=True, default='')
    recipient_group = models.ForeignKey(EmailGroup, related_name='sent_emails', null=True, blank=True)
    sender = models.EmailField(blank=True)
    subject = models.CharField(max_length=50, blank=True)
    message = models.TextField(max_length=500, blank=True)
    activity_list = models.CharField(max_length=500, blank=True)
    sent_time = models.DateTimeField(default = now)
    
    def __str__(self):
        return str(self.message)