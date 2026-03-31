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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔒 Solo artistas sin grupo
        self.fields['members'].queryset = Artist.objects.filter(groups__isnull=True)

        # 👇 PERMITIR los actuales si estamos editando
        if self.instance.pk:
            self.fields['members'].queryset |= self.instance.members.all()


    def clean_members(self):
        members = self.cleaned_data.get('members')

        for artist in members:
            if artist.groups.exclude(id=self.instance.id).exists():
                raise forms.ValidationError(
                    f"{artist} ya pertenece a otra agrupación"
                )

        return members