from django import forms
from .models import User

class CustomSignupForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    role = forms.ChoiceField(
        choices=[
            ('artist', 'Artista'),
            ('group_admin', 'Administrador de Agrupación'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    # 🔥 MÉTODO OBLIGATORIO
    def signup(self, request, user):
        user.role = self.cleaned_data['role']
        user.save()