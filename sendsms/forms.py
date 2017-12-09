from django import forms
from .models import SendSMS

class SendSMSForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = SendSMS
        fields = ['recipient_no', 'message']