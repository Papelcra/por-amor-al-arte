from django.urls import path
from . import views
from .views import generos_por_linea

app_name = 'catalog'

urlpatterns = [
    # Esta ruta manejará tanto la vista general como la filtrada
    path('', views.catalog_view, name='list'),
    path('generos/<int:linea_id>/', generos_por_linea, name='generos_por_linea'),
]