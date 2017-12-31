from django import forms
from .models import SMSMember

class SMSMemberForm(forms.ModelForm):
    class Meta:
        model = SMSMember
        fields = ('name', 'mobile', 'group', )