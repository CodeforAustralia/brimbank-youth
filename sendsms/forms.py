from django import forms
from .models import SendSMS, SendEmail

class SendSMSForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea)
    recipient_no = forms.CharField(widget=forms.TextInput(attrs={'type':'number'}))
    
    class Meta:
        model = SendSMS
        fields = ['recipient_no', 'message']

class SendEmailForm(forms.ModelForm):
    class Meta:
        model = SendEmail
        fields = ['sender', 'recipients', 'subject', 'message']