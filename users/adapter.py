from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):

        # ✅ RESPETA SI YA HAY UNA URL DESTINO
        next_url = request.GET.get('next')
        if next_url:
            return next_url

        user = request.user

        if user.role == 'artist':
            return reverse('artists:perfil')

        elif user.role == 'group_admin':
            return reverse('groups:mis_grupos')

        elif user.role == 'admin':
            return '/admin/'

        return super().get_login_redirect_url(request)