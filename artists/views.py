from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Artist, ArtistImage
from .forms import ArtistForm, ArtistImageForm
from catalog.models import Genre, LineaArtistica
from groups.models import Group


@login_required
def perfil_artista(request):
    if request.user.role != 'artist':
        return redirect('core:home')

    artist = Artist.objects.filter(user=request.user).first()

    if request.method == 'POST':
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
        'artista': artist,
    })


@login_required
def editar_perfil(request):
    if request.user.role != 'artist':
        messages.error(request, "No tienes permiso para editar un perfil de artista.")
        return redirect('core:home')

    artist, created = Artist.objects.get_or_create(user=request.user)
    lineas = LineaArtistica.objects.all()
    grupos = Group.objects.all()

    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES, instance=artist)

        if form.is_valid():
            artista = form.save(commit=False)
            artista.user = request.user

            # Línea artística
            linea_id = request.POST.get('linea')
            artista.linea_id = linea_id if linea_id else None

            # Grupo
            group_id = request.POST.get('group')

            group_id = request.POST.get('group')

            # 🔥 limpiar relaciones anteriores
            if artist.group:
                artist.group.members.remove(artist)

            if group_id:
                try:
                    grupo = Group.objects.get(id=group_id)
                    artista.group = grupo
                    artista.save()

                    # 🔥 sincronizar MANY TO MANY
                    grupo.members.add(artista)

                except Group.DoesNotExist:
                    artista.group = None
                    artista.save()
            else:
                artista.group = None
                artista.save()

            

            # Imágenes extra para el carrusel (máximo 3)
            imagenes_actuales = list(artist.images.order_by('order'))
            slots = ['extra_image_1', 'extra_image_2', 'extra_image_3']

            for i, slot in enumerate(slots):
                archivo = request.FILES.get(slot)
                if archivo:
                    if i < len(imagenes_actuales):
                        img_obj = imagenes_actuales[i]
                        img_obj.image = archivo
                        img_obj.save()
                    else:
                        if artist.images.count() < 3:
                            ArtistImage.objects.create(
                                artist=artista,
                                image=archivo,
                                order=i
                            )

            # Géneros (máximo 3)
            generos_ids = request.POST.getlist('genres')
            artista.genres.set(generos_ids[:3])

            messages.success(request, "¡Perfil actualizado con éxito!")
            return redirect('artists:ver_artista', artist_id=artista.id)

        else:
            messages.error(request, "Hubo un error en el formulario. Revisa los datos.")
    else:
        form = ArtistForm(instance=artist)

    imagenes = list(artist.images.order_by('order')[:3])
    while len(imagenes) < 3:
        imagenes.append(None)

    return render(request, 'artists/perfil.html', {
        'form': form,
        'lineas': lineas,
        'grupos': grupos,
        'artist': artist,
        'artista': artist,
        'imagenes_extra': imagenes,
    })


@login_required
def ver_perfil(request):
    if request.user.role != 'artist':
        return redirect('core:home')

    artist = get_object_or_404(Artist, user=request.user)
    return render(request, 'artists/ver.html', {
        'artista': artist,
        'artist': artist,
    })


def lista_artistas(request):
    artistas = (
        Artist.objects
        .select_related('linea', 'group')
        .prefetch_related('genres', 'images')
        .all()
    )

    genero_id = request.GET.get('genre')
    linea_id = request.GET.get('line')

    if genero_id:
        artistas = artistas.filter(genres__id=genero_id)

    if linea_id:
        artistas = artistas.filter(linea__id=linea_id)

    generos = Genre.objects.all()
    lineas = LineaArtistica.objects.all()

    return render(request, 'artists/lista.html', {
        'artistas': artistas,
        'generos': generos,
        'lineas': lineas,
    })


def ver_artista(request, artist_id):
    artista = get_object_or_404(Artist, id=artist_id)
    return render(request, 'artists/ver.html', {
        'artista': artista,
        'artist': artista,
    })


def get_grupo(request, artist_id):
    artista = get_object_or_404(Artist, id=artist_id)
    return JsonResponse({
        'group_id': artista.group.id if artista.group else None,
        'group_name': artista.group.name if artista.group else None,
    })


def get_artista_grupo(request, artista_id):
    artista = get_object_or_404(Artist, id=artista_id)
    return JsonResponse({
        'group_id': artista.group.id if artista.group else None,
        'group_name': artista.group.name if artista.group else None,
    })