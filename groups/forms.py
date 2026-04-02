from django import forms
from .models import Group
from artists.models import Artist

class GroupForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=Artist.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Seleccionar Miembros"
    )

    class Meta:
        model = Group
        fields = ['name', 'description', 'profile_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 💡 CAMBIO AQUÍ: Usamos 'member_of_groups' y 'group'
        self.fields['members'].queryset = Artist.objects.filter(
            member_of_groups__isnull=True, 
            group__isnull=True
        )

        if self.instance.pk:
            # Permitimos que los actuales miembros sigan apareciendo en la lista
            self.fields['members'].queryset |= self.instance.members.all()

    def clean_members(self):
        members = self.cleaned_data.get('members')
        for artist in members:
            # 💡 CAMBIO AQUÍ: Usamos 'member_of_groups'
            if artist.member_of_groups.exclude(id=self.instance.id).exists():
                raise forms.ValidationError(
                    f"{artist.stage_name} ya pertenece a otra agrupación."
                )
        return members