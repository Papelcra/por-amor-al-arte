from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class MyAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)

        # 👇 CAPTURAR EL ROLE DEL FORMULARIO
        role = request.POST.get('role')
        user.role = role  # asegúrate que este campo exista en tu modelo

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

        return super().get_login_redirect_url(request)