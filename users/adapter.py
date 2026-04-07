# users/adapter.py

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse
from users.models import User


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

    def pre_social_login(self, request, sociallogin):
        """
        Si el email de Google ya existe en nuestra base de datos, 
        conectamos la cuenta de Google al usuario existente automáticamente.
        """
        # 1. Si la cuenta ya está vinculada a un usuario, no hacemos nada
        if sociallogin.is_existing:
            return

        # 2. Extraer el email de los datos que vienen de Google
        # En Allauth moderno, el email viene dentro del diccionario 'extra_data'
        email = sociallogin.account.extra_data.get('email')

        if not email:
            return

        # 3. Intentar buscar al usuario por ese email
        try:
            user = User.objects.get(email=email)
            # Vincular la cuenta de Google al usuario que ya existía
            sociallogin.connect(request, user)
        except User.objects.DoesNotExist:
            # Si el usuario no existe, Allauth seguirá su curso y creará uno nuevo
            pass

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # Si el usuario es nuevo (acaba de ser creado por Google)
        if not user.role:
            user.role = 'artist' # Rol por defecto para nuevos de Google
            user.save()
        return user