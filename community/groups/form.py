from django import forms
from .models import Group, GroupMembers

class CreateGroupForm(forms.ModelForm):
    name = forms.CharField(required=True)


class GroupMembersForm(forms.ModelForm):
