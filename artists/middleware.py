# artists/middleware.py

from django.shortcuts import redirect
from .models import Artist

class CompleteProfileMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:

            allowed_paths = [
                '/artists/perfil/',
                '/artists/ver/',
                '/accounts/',        # ← cubre logout, login, google callback
                '/admin/',
                '/core/',            # ← FIX: evita el loop con home_artist
                '/media/',
                '/static/',
            ]

            if any(request.path.startswith(path) for path in allowed_paths):
                return self.get_response(request)

            if request.user.role == 'artist':
                try:
                    artist = Artist.objects.get(user=request.user)

                    if (
                        not artist.stage_name or
                        not artist.description or
                        not artist.genres.exists()
                    ):
                        return redirect('/artists/perfil/')  # ← FIX: redirige a perfil, no a home_artist

                except Artist.DoesNotExist:
                    return redirect('/artists/perfil/')

        return self.get_response(request)