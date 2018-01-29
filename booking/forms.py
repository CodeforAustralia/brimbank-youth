from django import forms
from django.forms import extras, ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ('first_name', 'surname', 'email', 'mobile_number', 'gender')
        labels = {
            'gender': _('Male or Female'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Type your first name here'}),
            'surname': forms.TextInput(attrs={'placeholder': 'Type your surname here'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Enter your mobile number'}),
        }