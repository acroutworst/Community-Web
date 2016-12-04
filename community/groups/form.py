from django import forms
from .models import Group

class CreateGroupForm(forms.ModelForm):
    name = forms.CharField(required=True)
    title = forms.CharField(required=True)
    description = forms.CharField()
    #current_leader = forms.CharField()

    class Meta:
        model = Group
        #fields = ['name', 'title', 'description', 'current_leader']
        fields = ['name', 'title', 'description']

#class JoinGroupForm(forms.ModelForm):
    #class Meta:
        #model = Group