from django import forms
from .models import Meetup, Attendee


class CreateMeetupForm(forms.ModelForm):
    name = forms.CharField(required=True)
    duration = forms.IntegerField(min_value=1, required=True)
    max_attendees = forms.IntegerField(min_value=1, required=False)
    description = forms.Textarea
    private = forms.NullBooleanSelect()

    class Meta:
        model = Meetup
        fields = ['name', 'duration', 'max_attendees', 'description', 'private']


class AttendMeetupForm(forms.ModelForm):
    status = forms.ChoiceField(required=True, choices=Attendee.STATUS_CHOICES)

    class Meta:
        model = Attendee
        fields = ['status']