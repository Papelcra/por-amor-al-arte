from django import forms
from .models import Group
from artists.models import Artist

class GroupForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=Artist.objects.all(),   # ← Empezamos con todos
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Seleccionar Miembros"
    )

    class Meta:
        model = Group
        fields = ['name', 'description', 'profile_image', 'members']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Mostramos TODOS los artistas (los que ya están en grupo también pueden aparecer para edición)
        self.fields['members'].queryset = Artist.objects.all().order_by('stage_name')

        # Si estamos editando un grupo existente, aseguramos que sus miembros actuales aparezcan
        if self.instance.pk:
            current_members = self.instance.members.all()
            self.fields['members'].queryset = (self.fields['members'].queryset | current_members).distinct()