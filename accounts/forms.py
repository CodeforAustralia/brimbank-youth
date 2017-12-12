from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import Profile, GENDER

class SignUpForm(UserCreationForm):    
    class Meta:	
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        
		
class ProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER, required=False )
    birth_date = forms.DateField(input_formats=['%d %b %Y'])

    class Meta:
        model = Profile
        fields = ('mobile', 'gender', 'birth_date', 'bio', )
        labels = {
            'mobile': _('Mobile phone'),
        }