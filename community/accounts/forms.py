from django import forms
from .models import Profile


class ProfileEditForm(forms.ModelForm):
    interests = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ['interests',  'phone_number']
