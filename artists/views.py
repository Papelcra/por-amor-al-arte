from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Artist, ArtistImage
from .forms import ArtistForm, ArtistImageForm
from catalog.models import Genre, LineaArtistica
from django.contrib import messages
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
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Artist
from .forms import ArtistForm
from catalog.models import Genre, LineaArtistica
from groups.models import Group  # Asegúrate de tener esta importación

@login_required
def editar_perfil(request):
    # Seguridad: Solo usuarios con rol 'artist' pueden acceder
    if request.user.role != 'artist':
        messages.error(request, "No tienes permiso para editar un perfil de artista.")
        return redirect('core:home')

    # Obtener el perfil del artista vinculado al usuario actual o crearlo si no existe
    artist, created = Artist.objects.get_or_create(user=request.user)
    
    # Traer datos necesarios para los selects del template
    lineas = LineaArtistica.objects.all()
    # Traer todos los grupos para el selector (puedes filtrar si lo deseas)
    grupos = Group.objects.all()

    if request.method == 'POST':
        # Pasamos instance=artist para que Django sepa que estamos editando y no creando
        form = ArtistForm(request.POST, request.FILES, instance=artist)

        if form.is_valid():
            # commit=False nos permite manipular el objeto antes de guardarlo en la DB
            artista = form.save(commit=False)
            artista.user = request.user

            # 1. Procesar Línea Artística (Foreign Key)
            linea_id = request.POST.get('linea')
            if linea_id:
                artista.linea_id = linea_id
            else:
                artista.linea = None

            # 2. Procesar Grupo (Foreign Key)
            # El 'name' en el <select> de tu HTML debe ser "group"
            group_id = request.POST.get('group')
            if group_id:
                artista.group_id = group_id
            else:
                artista.group = None

            # Guardar el objeto principal
            artista.save()

            # 3. Procesar Géneros (Many-to-Many)
            # Usamos getlist porque son múltiples checkboxes con name="genres"
            generos_ids = request.POST.getlist('genres')
            
            if len(generos_ids) <= 3:
                artista.genres.set(generos_ids)
                messages.success(request, "¡Perfil actualizado con éxito!")
                return redirect('artists:ver_artista', artist_id=artista.id)
            else:
                messages.warning(request, "Se guardó el perfil, pero recuerda: solo se permiten máximo 3 géneros.")
                # Aún así guardamos los primeros 3 o dejamos los anteriores
                artista.genres.set(generos_ids[:3])
                return redirect('artists:ver_artista', artist_id=artista.id)
        else:
            messages.error(request, "Hubo un error en el formulario. Revisa los datos.")
    else:
        # Si es GET, cargamos el formulario con los datos actuales
        form = ArtistForm(instance=artist)

    return render(request, 'artists/perfil.html', {
        'form': form,
        'lineas': lineas,
        'grupos': grupos,
        'artist': artist,
    })


@login_required
def ver_perfil(request):
    if request.user.role != 'artist':
        return redirect('core:home')

    artist = get_object_or_404(Artist, user=request.user)
    return render(request, 'artists/ver.html', {'artista': artist})


def lista_artistas(request):
    # Cargamos 'linea' y 'group' de una sola vez
    artistas = Artist.objects.select_related('linea', 'group').prefetch_related('genres').all()

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
    return render(request, 'artists/ver.html', {'artista': artista})


from django.http import JsonResponse

def obtener_generos_por_linea(request):
    linea_id = request.GET.get('linea_id')
    generos = Genre.objects.filter(linea_id=linea_id).values('id', 'nombre')
    return JsonResponse(list(generos), safe=False)