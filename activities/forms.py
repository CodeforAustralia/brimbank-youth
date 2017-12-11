from django import forms
from django.forms import extras
from django.utils.translation import ugettext_lazy as _

from .models import Activity, ActivityType, ActivityDraft
		
class ActivityForm(forms.ModelForm):
    activity_type = forms.ModelChoiceField(queryset=ActivityType.objects.all(), empty_label='Select', label = "Type", required=False)
    start_date = forms.DateField(input_formats=['%d %b %Y'])
    end_date = forms.DateField(input_formats=['%d %b %Y'])
    
#    start_date = forms.DateField(widget=extras.SelectDateWidget(empty_label="Nothing"))
#    activity_type = forms.ChoiceField(choices=ACTIVITY_TYPE, required=False)
    # skillcategory = forms.ModelChoiceField(queryset=SkillCategory.objects.all(), empty_label='Select', label = "Skill category", required=False )
#    start_time = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'time'})) # type can be date or time
#    end_time = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'time'}))

    class Meta:
        model = Activity
        fields = ('name', 'location', 'activity_type', 'start_date', 'start_time', 'end_date', 'end_time', 'activity_img')
        labels = {
            'activity_img': _('Image/Flyer'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Activity name'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter suburb'}),
        }
        error_messages = {
            'name': {
                'required': _("Please enter the activity name"),
            },
            'start_date': {
                'invalid': _("The entered date is invalid"),
            },
        }

class ActivitySearchForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['location']
        
class ActivityDraftForm(forms.ModelForm):
    activity_type = forms.ModelChoiceField(queryset=ActivityType.objects.all(), empty_label='Select', label = "Type", required=False)
    start_date = forms.DateField(input_formats=['%d %b %Y'])
    end_date = forms.DateField(input_formats=['%d %b %Y'])
    class Meta:
        model = ActivityDraft
        fields = ('name', 'location', 'activity_type', 'start_date', 'start_time', 'end_date', 'end_time', 'activity_img')
        labels = {
            'activity_img': _('Image/Flyer'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Activity name'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter suburb'}),
        }
        error_messages = {
            'name': {
                'required': _("Please enter the activity name"),
            },
            'start_date': {
                'invalid': _("The entered date is invalid"),
            },
        }