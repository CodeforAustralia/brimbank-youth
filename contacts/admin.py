from django.contrib import admin

from .models import EmailGroup, EmailMember

admin.site.register(EmailGroup)
admin.site.register(EmailMember)
