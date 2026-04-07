from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    path('perfil/', views.perfil_artista, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar'),
    
    path('lista/', views.lista_artistas, name='lista'),

    # 🔥 Vista de artista (detalle)
    path('<int:artist_id>/', views.ver_artista, name='ver_artista'),

    # 🔥 Endpoint único para el grupo (usar ESTE en el fetch)
    path('<int:artista_id>/grupo/', views.get_artista_grupo, name='artista_grupo'),
]