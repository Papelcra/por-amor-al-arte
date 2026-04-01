from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Artist, ArtistImage
from .forms import ArtistForm, ArtistImageForm
from catalog.models import Genre, LineaArtistica

@login_required
def perfil_artista(request):
    if request.user.role != 'artist':
        return redirect('core:home')

    artist = Artist.objects.filter(user=request.user).first()

    if request.method == 'POST':
        if 'upload_image' in request.POST:

            print("ARTIST:", artist)
        print("FILES:", request.FILES)

        image_form = ArtistImageForm(request.POST, request.FILES)

        if image_form.is_valid() and artist:
            img = image_form.save(commit=False)
            img.artist = artist
            img.save()

        return redirect('artists:perfil')

    image_form = ArtistImageForm()
    images = artist.images.all() if artist else []
    return render(request, 'core/home_artist.html', {
        'image_form': image_form,
        'images': images,
        'artist': artist,
    })

@login_required
def editar_perfil(request):
    if request.user.role != 'artist':
        return redirect('core:home')

    artist = Artist.objects.filter(user=request.user).first()
    if not artist:
        artist = Artist(user=request.user)

    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            a = form.save(commit=False)
            a.user = request.user
            a.save()
            form.save_m2m()
            return redirect('artists:ver', id=a.id)
    else:
        form = ArtistForm(instance=artist)

    return render(request, 'artists/perfil.html', {'form': form})


@login_required
def ver_perfil(request):
    if request.user.role != 'artist':
        return redirect('core:home')
    artist = get_object_or_404(Artist, user=request.user)
    return render(request, 'artists/ver.html', {'artista': artist})


def lista_artistas(request):
    artistas = Artist.objects.all()
    genero_id = request.GET.get('genre')
    linea_id = request.GET.get('line')
    if genero_id:
        artistas = artistas.filter(genres__id=genero_id)
    if linea_id:
        artistas = artistas.filter(linea_artistica__id=linea_id)  # ← fix aquí
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