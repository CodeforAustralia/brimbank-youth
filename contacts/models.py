from django.db import models
from django.contrib.auth.models import User

GENDER = (
    ('F', 'Female'),
    ('M', 'Male'),
)

class ContactGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name

class SMSMember(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10, null=True)
    group = models.ForeignKey(ContactGroup, related_name='sms_members', null=True)

class EmailGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    staff = models.ForeignKey(User, related_name='contact_groups', null=True, db_index=True)
    
    def __str__(self):
        return self.name

    class Meta:
        index_together = ["staff"]

class EmailMember(models.Model):
    group = models.ForeignKey(EmailGroup, related_name='members', null=True, db_index=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=50, null=True)
    gender = models.CharField(max_length=15, choices=GENDER, default='F', null=True)
    mobile = models.CharField(max_length=10, null=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    language = models.CharField(max_length=60, null=True, blank=True)

    class Meta:
        index_together = ["group"]