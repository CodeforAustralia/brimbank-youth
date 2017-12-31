from django.db import models

# Create your models here.
class SMSMember(models.Model):
    GROUP_NAMES = (
        (1, 'Group A'),
        (2, 'Group B'),
        (3, 'Group C'),
    )
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10, null=True)
    group = models.PositiveSmallIntegerField(choices=GROUP_NAMES)