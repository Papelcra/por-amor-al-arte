from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    path('', views.lista_artistas, name='lista'),

    # editar perfil del artista logueado
    path('perfil/', views.perfil_artista, name='perfil'),

    # ver detalle de cualquier artista
    path('<int:id>/', views.ver_artista, name='ver_artista'),
]