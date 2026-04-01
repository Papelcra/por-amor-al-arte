from django import forms
from .models import Artist, ArtistImage
from catalog.models import Genre

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['stage_name', 'description', 'profile_image', 'genres']
        widgets = {
            'genres': forms.CheckboxSelectMultiple
        }

# ── NUEVO ──
class ArtistImageForm(forms.ModelForm):
    class Meta:
        model = ArtistImage
        fields = ['image']