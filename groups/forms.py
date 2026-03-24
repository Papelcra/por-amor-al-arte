from django import forms
from .models import Group
from artists.models import Artist

class GroupForm(forms.ModelForm):

    members = forms.ModelMultipleChoiceField(
        queryset=Artist.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'description', 'profile_image', 'members']