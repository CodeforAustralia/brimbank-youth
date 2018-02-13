from django import forms
from django.forms import extras, ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Activity, ActivityType, ActivityDraft, ACTIVITY_TYPES, SPACE_OPTIONS, COST_OPTIONS, LISTING_PRIVACY

import arrow

def file_size(value):
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File size is too large. The size should not exceed 2MB')

class ActivityForm(forms.ModelForm):
    activity_type = forms.ChoiceField(choices=ACTIVITY_TYPES, label='What type of activity are you creating ?', required=False)
    start_date = forms.DateField(input_formats=['%d %b %Y'], label='OCCURS FROM', required=False)
    end_date = forms.DateField(input_formats=['%d %b %Y'], label='OCCURS UNTIL', required=False)
    activity_img = forms.ImageField(validators=[file_size], label='Add an event image', required=False)
    flyer = forms.FileField(validators=[file_size], label='Upload a printable event flyer', required=False)
    
    def __init__(self, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].required = True
        self.fields['location'].required = True

    class Meta:
        model = Activity
        fields = ('activity_type', 'name', 'location', 'term', 'start_time', 'end_time', 'start_date', 'end_date', 
        'activity_date', 'activity_day', 'description','organiser', 'contact_number', 'activity_img', 'flyer', 
        'space_choice', 'space', 'cost_choice', 'cost', 'min_age', 'max_age', 'background', 'gender', 'living_duration', 
        'listing_privacy', 'suburb', 'postcode')
        labels = {
#            'activity_img': _('Add an event image'),
            'name': _('What is the name of the activity ?'),
            'location': _('Where is the location ?'),
            'start_time': _('FROM'),
            'end_time': _('TO'),
            'description': _('Describe the event'),
            'organiser': _('Organiser details'),
            'contact_number': _('Contact number'),
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
            'background':_('Language(s) spoken'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Give a short distinct name'}),
            'location': forms.TextInput(attrs={'placeholder': 'Search for an address'}),
            'space_choice': forms.RadioSelect(choices=SPACE_OPTIONS),
            'cost_choice': forms.RadioSelect(choices=COST_OPTIONS),
            'listing_privacy': forms.RadioSelect(choices=LISTING_PRIVACY),
            'min_age': forms.TextInput(attrs={'placeholder': 'Minimum age'}),
            'max_age': forms.TextInput(attrs={'placeholder': 'Maximum age'}),
            'organiser': forms.TextInput(attrs={'placeholder': 'Contact person'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Contact number'}),
            'suburb': forms.TextInput(attrs={'placeholder': 'Suburb', 'data-geo':'locality'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'Postcode', 'data-geo':'postal_code'}),
        }
        error_messages = {
            'name': {
                'required': _("Please enter the activity name"),
            },
            'start_date': {
                'invalid': _("The entered date is invalid"),
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        activity_date = cleaned_data.get("activity_date")
        activity_day = cleaned_data.get("activity_day")
        term = cleaned_data.get("term")
        if term != 'Once':
            if start_date and end_date:
                begin_date = arrow.get(start_date, 'Australia/Melbourne')
                finish_date = arrow.get(end_date, 'Australia/Melbourne')
                if begin_date > finish_date:
                    msg = "Start date must be before end date."
                    self.add_error('start_date', msg)
                    self.add_error('end_date', msg)
                if activity_day != begin_date.format('dddd') and term != 'Daily':
                    msg = "Activity must occur at the same day as the start date."
                    self.add_error('start_date', msg)
                    self.add_error('activity_day', msg)
            else:
                if not start_date:
                    msg = "Start date must be entered."
                    self.add_error('start_date', msg)
                if not end_date:
                    msg = "End date must be entered."
                    self.add_error('end_date', msg)
        else:
            if not activity_date:
                msg = "Activity date must be entered."
                self.add_error('activity_date', msg)

class ActivitySearchForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['location']

class ShareURLForm(forms.Form):
    url = forms.CharField(max_length=300)
        
class ActivityDraftForm(forms.ModelForm):
    activity_type = forms.ChoiceField(choices=ACTIVITY_TYPES, required=False, label='What type of activity are you creating ?')
    start_date = forms.DateField(input_formats=['%d %b %Y'], label='OCCURS FROM', required=False)
    end_date = forms.DateField(input_formats=['%d %b %Y'], label='OCCURS UNTIL', required=False)
    activity_img = forms.ImageField(required=False, validators=[file_size], label='Add an event image')
    flyer = forms.FileField(required=False, validators=[file_size], label='Upload a printable event flyer')
                           
    class Meta:
        model = ActivityDraft
        fields = ('activity_type', 'name', 'location', 'term', 'start_time', 'end_time', 'start_date', 'end_date', 
        'activity_date', 'activity_day', 'description','organiser', 'contact_number', 'activity_img', 'flyer', 
        'space_choice', 'space', 'cost_choice', 'cost', 'min_age', 'max_age', 'background', 'gender', 
        'living_duration', 'listing_privacy', 'suburb', 'postcode')
        labels = {
#            'activity_img': _('Add an event image'),
            'name': _('What is the name of the activity ?'),
            'location': _('Where is the location ?'),
            'start_time': _('FROM'),
            'end_time': _('TO'),
            'description': _('Describe the event'),
            'organiser': _('Organiser details'),
            'contact_number': _('Contact number'),
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
            'background':_('Language(s) spoken'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Give a short distinct name'}),
            'location': forms.TextInput(attrs={'placeholder': 'Search for an address'}),
            'space_choice': forms.RadioSelect(choices=SPACE_OPTIONS),
            'cost_choice': forms.RadioSelect(choices=COST_OPTIONS),
            'listing_privacy': forms.RadioSelect(choices=LISTING_PRIVACY),
            'min_age': forms.TextInput(attrs={'placeholder': 'Minimum age'}),
            'max_age': forms.TextInput(attrs={'placeholder': 'Maximum age'}),
            'organiser': forms.TextInput(attrs={'placeholder': 'Contact person'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Contact number'}),
            'suburb': forms.TextInput(attrs={'placeholder': 'Suburb', 'data-geo':'locality'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'Postcode', 'data-geo':'postal_code'}),
        }
        error_messages = {
            'name': {
                'required': _("Please enter the activity name"),
            },
            'start_date': {
                'invalid': _("The entered date is invalid"),
            },
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        term = cleaned_data.get("term")
        activity_day = cleaned_data.get("activity_day")
        if term != 'Once':
            if start_date and end_date:
                begin_date = arrow.get(start_date, 'Australia/Melbourne')
                print(begin_date.format('dddd'))
                finish_date = arrow.get(end_date, 'Australia/Melbourne')
                # Validation: start_date must be before end_date
                if begin_date > finish_date:
                    msg = "Start date must be before end date."
                    self.add_error('start_date', msg)
                    self.add_error('end_date', msg)
                if activity_day != begin_date.format('dddd') and term != 'Daily':
                    msg = "Activity must occur at the same day as the start date."
                    self.add_error('start_date', msg)
                    self.add_error('activity_day', msg)  

#    def clean(self):
#        cleaned_data = super().clean()
#        start_date = cleaned_data.get("start_date")
#        end_date = cleaned_data.get("end_date")
#        term = cleaned_data.get("term")
#        
#        if term != 'Once':
#            begin_date = arrow.get(start_date, 'Australia/Melbourne')
#            finish_date = arrow.get(end_date, 'Australia/Melbourne')
#            if finish_date < begin_date:
#                msg = "Must put 'help' in subject when cc'ing yourself."
#                self.add_error('start_date', msg)
#                self.add_error('end_date', msg)