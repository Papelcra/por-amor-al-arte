from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Artist
from .forms import ArtistForm
from catalog.models import Genre, LineaArtistica

@login_required
def perfil_artista(request):
    # Obtener o crear el perfil del artista vinculado al usuario
    artist, created = Artist.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES, instance=artist)

        if form.is_valid():
            artist = form.save(commit=False)
            artist.save()

            form.save_m2m()  # 👈 PRIMERO guarda los géneros

            # 🎯 AHORA sí puedes acceder correctamente
            generos = artist.genres.all()

            if generos.exists():
                artist.group = generos.first().linea
                artist.save()  # 👈 guardar el cambio

            return redirect('core:home')

    else:
        form = ArtistForm(instance=artist)

    return render(request, 'artists/perfil.html', {'form': form})

from django.shortcuts import render
from .models import Artist
from catalog.models import Genre

def lista_artistas(request):

    artistas = Artist.objects.all()

    # filtros
    genero_id = request.GET.get('genre')
    linea_id = request.GET.get('line')

    if genero_id:
        artistas = artistas.filter(genres__id=genero_id)

    if linea_id:
        artistas = artistas.filter(group__id=linea_id)

    # datos para filtros
    generos = Genre.objects.all()
    lineas = LineaArtistica.objects.all()

    return render(request, 'artists/lista.html', {
        'artistas': artistas,
        'generos': generos,
        'lineas': lineas,
    })

def ver_artista(request, id):
    artista = get_object_or_404(Artist, id=id)
    return render(request, 'artists/ver.html', {'artista': artista})