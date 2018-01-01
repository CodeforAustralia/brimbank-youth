from django import forms
from .models import SMSMember, ContactGroup

class ContactGroupForm(forms.ModelForm):
    class Meta:
        model = ContactGroup
        fields = ('name', 'description', )

class SMSMemberForm(forms.ModelForm):
    class Meta:
        model = SMSMember
        fields = ('name', 'mobile', 'group', )