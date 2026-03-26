from django import forms
from .models import User


class CustomSignupForm(forms.Form):

    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def signup(self, request, user):
        user.role = self.cleaned_data['role']
        user.save()