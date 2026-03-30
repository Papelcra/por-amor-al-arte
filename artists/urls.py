from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    path('perfil/', views.perfil_artista, name='perfil'),
    path('lista/', views.lista_artistas, name='lista'),
    path('ver/<int:id>/', views.ver_artista, name='ver'),
    
]