from django import forms
from .models import Artist
from catalog.models import Genre

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['stage_name', 'description', 'profile_image', 'genres']
        widgets = {
            'genres': forms.CheckboxSelectMultiple
        }