from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Esta ruta manejará tanto la vista general como la filtrada
    path('', views.catalog_view, name='list'),
]