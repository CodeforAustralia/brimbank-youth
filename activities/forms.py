from django import forms
from django.forms import extras
from django.utils.translation import ugettext_lazy as _

from .models import Activity, ActivityType, ActivityDraft
		
class ActivityForm(forms.ModelForm):
    activity_type = forms.ModelChoiceField(queryset=ActivityType.objects.all(), required=False)
    start_date = forms.DateField(input_formats=['%d %b %Y'])
    end_date = forms.DateField(input_formats=['%d %b %Y'])
    
#    start_date = forms.DateField(widget=extras.SelectDateWidget(empty_label="Nothing"))
#    activity_type = forms.ChoiceField(choices=ACTIVITY_TYPE, required=False)
    # skillcategory = forms.ModelChoiceField(queryset=SkillCategory.objects.all(), empty_label='Select', label = "Skill category", required=False )
#    start_time = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'time'})) # type can be date or time
#    end_time = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'time'}))

    class Meta:
        model = Activity
        fields = ('name', 'location', 'activity_type', 'start_date', 'start_time', 'end_date', 'end_time', 'description','activity_img', 'flyer')
        labels = {
            'activity_img': _('Add an event image'),
            'activity_type': _('What type of activity are you creating ?'),
            'name': _('What is the name of the activity ?'),
            'location': _('Where is the location ?'),
            'start_time': _('FROM'),
            'end_time': _('TO'),
            'start_date': _('OCCURS FROM'),
            'end_date': _('OCCURS UNTIL'),
            'description': _('Describe the event'),
            'organiser': _('Organiser Details'),
            'flyer': _('Upload an event flyer'),
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
    activity_type = forms.ModelChoiceField(queryset=ActivityType.objects.all(), required=False, label='What type of activity are you creating ?')
    start_date = forms.DateField(input_formats=['%d %b %Y'], label='OCCURS FROM', required=False)
    end_date = forms.DateField(input_formats=['%d %b %Y'], label='OCCURS UNTIL', required=False)
    class Meta:
        model = ActivityDraft
        fields = ('activity_type', 'name', 'location', 'term', 'start_time', 'end_time', 'start_date', 'end_date', 'activity_date', 'activity_day', 'description','organiser', 'activity_img', 'flyer')
        labels = {
            'activity_img': _('Add an event image'),
            'name': _('What is the name of the activity ?'),
            'location': _('Where is the location ?'),
            'start_time': _('FROM'),
            'end_time': _('TO'),
            'description': _('Describe the event'),
            'organiser': _('Organiser details'),
            'flyer': _('Upload an event flyer'),
            'term': _('HOW OFTEN DOES THIS EVENT OCCUR'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Give a short distinct name'}),
            'location': forms.TextInput(attrs={'placeholder': 'Search for an address'}),
        }
        error_messages = {
            'name': {
                'required': _("Please enter the activity name"),
            },
            'start_date': {
                'invalid': _("The entered date is invalid"),
            },
        }