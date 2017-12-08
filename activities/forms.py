from django import forms
from django.forms import extras

from .models import Activity, ActivityType
		
class ActivityForm(forms.ModelForm):
    activity_type = forms.ModelChoiceField(queryset=ActivityType.objects.all(), empty_label='Select', label = "Type", required=False)
    start_date = forms.DateField(widget=extras.SelectDateWidget(empty_label="Nothing"))
#    activity_type = forms.ChoiceField(choices=ACTIVITY_TYPE, required=False)
    # skillcategory = forms.ModelChoiceField(queryset=SkillCategory.objects.all(), empty_label='Select', label = "Skill category", required=False )
#    start_time = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'time'})) # type can be date or time
#    end_time = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'time'}))

    class Meta:
        model = Activity
        fields = ('name', 'activity_type', 'start_date', 'start_time', 'end_date', 'end_time', 'activity_img')
##        labels = {
#            'mobile': _('Mobile phone'),
#        }
#        widgets = {
#            'email': forms.TextInput(attrs={'placeholder': 'jane@example.com'}),
#            'bio': forms.Textarea(attrs={'placeholder': 'Tell us a bit about yourself'}),
#            'skill': Select2MultipleWidget(choices=SKILLS)
#        }
		