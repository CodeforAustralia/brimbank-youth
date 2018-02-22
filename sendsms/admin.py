from django.contrib import admin

from .models import SendSMS, SendEmail

# Register your models here.

admin.site.register(SendSMS)
admin.site.register(SendEmail)