from django.shortcuts import redirect
from .models import Artist

class CompleteProfileMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:

            # Rutas que NO deben redirigir (para evitar loops)
            allowed_paths = [
                    '/artists/perfil/',
                    '/artists/ver/',
                    '/accounts/logout/',
                    '/admin/',
            ]

            if any(request.path.startswith(path) for path in allowed_paths):
                return self.get_response(request)

            if request.user.role == 'artist':
                try:
                    artist = Artist.objects.get(user=request.user)

                    # 🔥 Validación completa
                    if (
                        not artist.stage_name or
                        not artist.description or
                        not artist.genres.exists()
                    ):
                        return redirect('/artists/perfil/')

                except Artist.DoesNotExist:
                    return redirect('/artists/perfil/')

        return self.get_response(request)