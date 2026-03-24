from django.shortcuts import render

def home(request):
    # 👤 Usuario NO autenticado -> Ver base pública de artistas
    if not request.user.is_authenticated:
        return render(request, 'core/home_public.html')

    # 🎨 Redirección por Rol [cite: 5-7, 16]
    if request.user.role == 'artist':
        return render(request, 'core/home_artist.html')

    elif request.user.role == 'group_admin':
        return render(request, 'core/home_admin.html')

    # Fallback por si no tiene rol asignado
    return render(request, 'core/home_public.html')