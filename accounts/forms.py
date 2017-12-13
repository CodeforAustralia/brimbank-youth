from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import Profile, GENDER

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:	
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'organisation_name', 'description')
        labels = {
            'mobile': _('Mobile phone'),
        }