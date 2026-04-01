# users/adapter.py

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse


class MyAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        role = request.POST.get('role')
        if role:  # ← FIX: solo asigna si viene el campo (registro normal)
            user.role = role
        if commit:
            user.save()
        return user

    def get_login_redirect_url(self, request):
        next_url = request.GET.get('next')
        if next_url:
            return next_url

        user = request.user

        if user.role == 'artist':
            return reverse('artists:perfil')
        elif user.role == 'group_admin':
            return reverse('groups:mis_grupos')
        elif user.is_superuser:
            return '/admin/'

        return '/core/'  # ← FIX: fallback seguro si no tiene role


# ✅ FIX: Adapter para Google — asigna role por defecto
class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        if not user.role:          # si Google no trajo role, asigna uno por defecto
            user.role = 'artist'   # ← cambia según tu lógica de negocio
            user.save()
        return user