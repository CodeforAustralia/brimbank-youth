from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.forms import extras, ValidationError

from .models import Profile, GENDER

def file_size(value):
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File size is too large. The size should not exceed 1MB')

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget=forms.TextInput(
           attrs={'type': 'email',
           'placeholder': _('E-mail address')}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Must contain at least 8 characters'}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={'placeholder': 'Enter the same password'}))

    def __init__(self,*args,**kwargs):
        kwargs.setdefault('label_suffix', '')
        super(SignUpForm,self).__init__(*args,**kwargs)

    class Meta:	
        model = User
        fields = ('email', 'username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Your username'}),
        }
        
class ProfileForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ProfileForm,self).__init__(*args,**kwargs)

    class Meta:
        model = Profile
        fields = ('organisation_name', 'address', 'web_address', 'staff_name', 'role', 'phone', 'description',)
        labels = {
            'organisation_name': _('What organisation do you work for?'),
            'address': _('What is the address of your organisation?'),
            'web_address': _('What is your organisation\'s website address?'),
            'staff_name': _('What is your name?'),
            'role': _('What is your role at this organisation?'),
            'phone': _('What is the best number to contact you on?'),
            'description': _('Describe what your organisation does in 300 words or less'),
        }
        widgets = {
            'web_address': forms.TextInput(attrs={'placeholder': 'e.g. http://www.example.com'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter your address'}),
            'role': forms.TextInput(attrs={'placeholder': 'e.g. Youth Worker'}),
            'description': forms.Textarea(attrs={'rows':4, 'cols':8}),
        }