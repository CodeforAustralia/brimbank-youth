from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import SMSMember, ContactGroup, EmailGroup, EmailMember
from activities.models import Activity

class ContactGroupForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ContactGroupForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ContactGroup
        fields = ('name', 'description', )
        labels = {
            'name': _('Group Name'),
        }

class SMSMemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(SMSMemberForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SMSMember
        fields = ('name', 'mobile', )

class EmailGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(EmailGroupForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = EmailGroup
        fields = ('name', )
        labels = {
            'name': _('Group Name'),
        }

class EmailMemberForm(forms.ModelForm):
    age = forms.CharField(error_messages={'required': 'Required'})

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(EmailMemberForm, self).__init__(*args, **kwargs)

    class Meta:
        model = EmailMember
        fields = ('first_name', 'last_name', 'email', 'gender', 'age', 'mobile', 'language', )
        labels = {
            'gender': _('M or F'),
            'mobile': _('Mobile no'),
            'language': _('Languages Spoken'),
        }
        error_messages = {
            'first_name': {
                'required': _('Required'),
            },
            'last_name': {
                'required': _('Required'),
            },
            'email': {
                'required': _('Required'),
            },
            'mobile': {
                'required': _('Required'),
            },
        }

class ActivityListForm(forms.Form):
    activities = forms.ModelMultipleChoiceField(queryset=Activity.objects.all())