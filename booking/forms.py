from django import forms
from django.forms import extras, ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Registration
from activities.models import Activity

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ('first_name', 'surname', 'email', 'mobile_number', 'gender', 'age', 'language')
        labels = {
            'gender': _('Male or Female'),
            'language': _('Languages spoken'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Type your first name here'}),
            'surname': forms.TextInput(attrs={'placeholder': 'Type your surname here'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Enter your mobile number'}),
        }

    def __init__(self,*args,**kwargs):
        activity_pk = kwargs.pop('activity_pk', None)
        self.activity = Activity.objects.get(pk=activity_pk)
        super(RegistrationForm,self).__init__(*args,**kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        mobile_number = cleaned_data.get('mobile_number')
        email_existed = Registration.objects.filter(email=email, activity=self.activity)
        mobile_existed = None
        if mobile_number:
            mobile_existed = Registration.objects.filter(mobile_number=mobile_number, activity=self.activity)
        if email_existed or mobile_existed:
            msg = 'You have registered for this event. Only one registration is allowed.'
            raise ValidationError(msg)