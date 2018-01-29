from django.db import models

from activities.models import Activity

GENDER = (
    ('F', 'Female'),
    ('M', 'Male'),
)

# Create your models here.
class Registration(models.Model):
    first_name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=15, choices=GENDER, default='F')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.first_name, self.surname)
