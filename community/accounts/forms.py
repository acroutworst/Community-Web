from django import forms
from .models import Profile, ProfileImage


class ProfileEditForm(forms.ModelForm):
    interests = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)


    class Meta:
        model = Profile
        fields = ['interests', 'phone_number']


class ProfileImageUploadForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = ProfileImage
        fields = ['image']


class ProfileImageSelectForm(forms.ModelForm):
    image = forms.ChoiceField()

    class Meta:
        model = Profile
        fields = ['image']