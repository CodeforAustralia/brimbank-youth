from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import SendSMS, SendEmail

class SendSMSForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter additional message here...'}))
    activity_list = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly'}))
    # recipient_no = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}))
    
    class Meta:
        model = SendSMS
        fields = ['recipient_no', 'recipient_group', 'message', 'activity_list', ]
        widgets = {
            'recipient_no': forms.TextInput(attrs={'placeholder': 'Separate mobile numbers by comma'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Validation: either recipient_group or recipient_no must be entered
        recipient_no = cleaned_data.get("recipient_no")
        recipient_group = cleaned_data.get("recipient_group")
        if recipient_no == '' and recipient_group is None:
            msg = "Either recipient number or recipient group must be entered."
            self.add_error('recipient_no','')
            self.add_error('recipient_group','')
            raise forms.ValidationError(msg)

class SendEmailForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter additional message here...'}))
    activity_list = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly'}))
    class Meta:
        model = SendEmail
        fields = ['sender', 'recipients', 'recipient_group', 'subject', 'message', 'activity_list',]
        widgets = {
            'recipients': forms.TextInput(attrs={'placeholder': 'Separate email addresses by comma'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Validation: either recipients or recipient_no must be entered
        recipients = cleaned_data.get("recipients")
        recipient_group = cleaned_data.get("recipient_group")
        if recipients == '' and recipient_group is None:
            msg = "Either recipients or recipient group must be entered."
            self.add_error('recipients','')
            self.add_error('recipient_group','')
            raise forms.ValidationError(msg)