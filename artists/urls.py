from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    path('perfil/', views.perfil_artista, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar'),  # ← NUEVA
    path('lista/', views.lista_artistas, name='lista'),
    path('<int:artist_id>/', views.ver_artista, name='ver_artista'),
]