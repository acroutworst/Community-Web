from django import forms
from .models import UserProfile


class ProfileEditForm(forms.ModelForm):
    department = forms.CharField(required=False)
    position = forms.CharField(required=False)
    interests = forms.CharField(required=False)
    transportation = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)

    class Meta:
        model = UserProfile
        fields = ['position', 'department', 'interests', 'transportation', 'phone_number']