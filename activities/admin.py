from django.contrib import admin

from .models import Activity, ActivityType, ActivityDraft

# Register your models here.
admin.site.register(ActivityType)
admin.site.register(Activity)
admin.site.register(ActivityDraft)