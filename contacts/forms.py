from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import SMSMember, ContactGroup, EmailGroup, EmailMember

class ContactGroupForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = ContactGroup
        fields = ('name', 'description', )
        labels = {
            'name': _('Group Name'),
        }

class SMSMemberForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=ContactGroup.objects.all())
    class Meta:
        model = SMSMember
        fields = ('group', 'name', 'mobile', )

class EmailGroupForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = EmailGroup
        fields = ('name', 'description', )

class EmailMemberForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=EmailGroup.objects.all())
    class Meta:
        model = EmailMember
        fields = ('group', 'name', 'email', )