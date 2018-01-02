from django import forms
from .models import SMSMember, ContactGroup

class ContactGroupForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = ContactGroup
        fields = ('name', 'description', )

class SMSMemberForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=ContactGroup.objects.all())
    class Meta:
        model = SMSMember
        fields = ('group', 'name', 'mobile', )