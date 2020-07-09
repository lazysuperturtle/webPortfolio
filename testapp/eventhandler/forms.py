from django import forms
from models import User, Event

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
