from django.db import models

# Create your models here.
class ContactGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name

class SMSMember(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10, null=True)
    group = models.ForeignKey(ContactGroup, related_name='sms_members', null=True)