from django import forms
from .models import Event

class EventSearchForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['city']