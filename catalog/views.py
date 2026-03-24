from django.shortcuts import render
from artists.models import Artist
from groups.models import Group

def catalog_view(request):
    linea_id = request.GET.get('linea')
    
    artistas = Artist.objects.all()
    agrupaciones = Group.objects.all()

    if linea_id:
        # Usamos 'linea' que es el nombre del campo en el modelo Genre
        artistas = artistas.filter(genres__linea__id=linea_id).distinct()
        agrupaciones = agrupaciones.filter(genres__linea__id=linea_id).distinct()

    context = {
        'artistas': artistas,
        'agrupaciones': agrupaciones,
        'linea_id': linea_id
    }
    return render(request, 'catalog/list.html', context)