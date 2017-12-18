from django import forms
from django.forms import extras
from django.utils.translation import ugettext_lazy as _

from .models import Activity, ActivityType, ActivityDraft, ACTIVITY_TYPES, SPACE_OPTIONS, COST_OPTIONS, LISTING_PRIVACY
		
class ActivityForm(forms.ModelForm):
    activity_type = forms.ChoiceField(choices=ACTIVITY_TYPES, required=False, label='What type of activity are you creating ?')
    start_date = forms.DateField(input_formats=['%d %b %Y'])
    end_date = forms.DateField(input_formats=['%d %b %Y'])
    
#    start_date = forms.DateField(widget=extras.SelectDateWidget(empty_label="Nothing"))
#    activity_type = forms.ChoiceField(choices=ACTIVITY_TYPE, required=False)
    # skillcategory = forms.ModelChoiceField(queryset=SkillCategory.objects.all(), empty_label='Select', label = "Skill category", required=False )
#    start_time = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'time'})) # type can be date or time
#    end_time = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'time'}))

    class Meta:
        model = Activity
        fields = ('activity_type', 'name', 'location', 'activity_type', 'start_date', 'start_time', 'end_date', 'end_time', 'description','activity_img', 'flyer')
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
    activity_type = forms.ChoiceField(choices=ACTIVITY_TYPES, required=False, label='What type of activity are you creating ?')
    start_date = forms.DateField(input_formats=['%d %b %Y'], label='OCCURS FROM', required=False)
    end_date = forms.DateField(input_formats=['%d %b %Y'], label='OCCURS UNTIL', required=False)
    
#    def __init__(self, *args, **kwargs):
#       self.request = kwargs.pop('request', None)
#       return super(ActivityDraftForm, self).__init__(*args, **kwargs)
#    
#    def save(self, *args, **kwargs):
#       kwargs['commit']=False
#       obj = super(ActivityDraftForm, self).save(*args, **kwargs)
#       if self.request:
#           obj.user = self.request.user
#       obj.save()
#       return obj
    
    class Meta:
        model = ActivityDraft
        fields = ('activity_type', 'name', 'location', 'term', 'start_time', 'end_time', 'start_date', 'end_date', 'activity_date', 'activity_day', 'description','organiser', 'activity_img', 'flyer', 'space_choice', 'space', 'cost_choice', 'cost', 'min_age', 'max_age', 'background', 'gender', 'living_duration', 'listing_privacy')
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
            'space': _('Space'),
            'cost': _('Cost'),
            'cost_choice': _('Is there a cost ?'),
            'living_duration': _('Living in Australia'),
            'listing_privacy': _('Listing Privacy'),
            'min_age': _('From age'),
            'max_age': _('To age'),
            'listing_privacy': _('Listing Privacy'),
            'space_choice':_('Create the number of spaces available'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Give a short distinct name'}),
            'location': forms.TextInput(attrs={'placeholder': 'Search for an address'}),
            'space_choice': forms.RadioSelect(choices=SPACE_OPTIONS),
            'cost_choice': forms.RadioSelect(choices=COST_OPTIONS),
            'listing_privacy': forms.RadioSelect(choices=LISTING_PRIVACY),
            'min_age': forms.TextInput(attrs={'placeholder': 'Minimum age'}),
            'max_age': forms.TextInput(attrs={'placeholder': 'Maximum age'}),
        }
        error_messages = {
            'name': {
                'required': _("Please enter the activity name"),
            },
            'start_date': {
                'invalid': _("The entered date is invalid"),
            },
        }