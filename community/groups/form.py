from django import forms
from .models import Group

class CreateGroupForm(forms.ModelForm):
    title = forms.CharField(required=True)
    description = forms.CharField()
    #current_leader = forms.CharField()

    class Meta:
        model = Group
        #fields = ['name', 'title', 'description', 'current_leader']
        fields = ['title', 'description']

#class JoinGroupForm(forms.ModelForm):
    #class Meta:
        #model = Group