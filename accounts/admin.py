from django.contrib import admin

from .models import Profile, AdminEmail

# Register your models here.
admin.site.register(Profile)
admin.site.register(AdminEmail)