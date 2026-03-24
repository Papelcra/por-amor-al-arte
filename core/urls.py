from django.urls import path
from . import views

app_name = 'core'  # <--- ESTA LÍNEA ES LA QUE FALTA

urlpatterns = [
    path('', views.home, name='home'),
]