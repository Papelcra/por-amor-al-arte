from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Artist
from .forms import ArtistForm
from catalog.models import Genre, LineaArtistica
from django.contrib import messages

# 🎨 PERFIL ARTISTA
@login_required
def perfil_artista(request):
    if request.user.role != 'artist':
        return redirect('core:home')

    artist = Artist.objects.filter(user=request.user).first()
    if not artist:
        artist = Artist(user=request.user)

    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            artist = form.save(commit=False)
            artist.user = request.user
            artist.save()
            form.save_m2m()
            # 🔹 Redirige a la página de ver perfil
            return redirect('artists:ver', id=artist.id)
        else:
            print("❌ ERRORES:", form.errors)
    else:
        form = ArtistForm(instance=artist)

    return render(request, 'artists/perfil.html', {'form': form})
# 📋 LISTA DE ARTISTAS
def lista_artistas(request):

    artistas = Artist.objects.all()

    # filtros
    genero_id = request.GET.get('genre')
    linea_id = request.GET.get('line')

    if genero_id:
        artistas = artistas.filter(genres__id=genero_id)

    if linea_id:
        artistas = artistas.filter(group__id=linea_id)

    generos = Genre.objects.all()
    lineas = LineaArtistica.objects.all()

    return render(request, 'artists/lista.html', {
        'artistas': artistas,
        'generos': generos,
        'lineas': lineas,
    })


def ver_artista(request, id):
    print("🔥 ENTRE A VER_ARTISTA")
    artista = get_object_or_404(Artist, id=id)
    return render(request, 'artists/ver.html', {'artista': artista})

