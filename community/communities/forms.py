from django import forms
from .models import CommunityUserProfile


class CreateCommunityProfileForm(forms.ModelForm):
    department = forms.CharField(required=False)
    position = forms.CharField(required=False)

    class Meta:
        model = CommunityUserProfile
        fields = ['department',  'position']