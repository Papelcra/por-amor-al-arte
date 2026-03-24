from django.urls import path
from .views import crear_grupo, lista_grupos,ver_grupo,editar_grupo,mis_grupos

urlpatterns = [
    path('', lista_grupos, name='lista_grupos'),  # 👈 ESTA FALTABA
    path('crear/', crear_grupo, name='crear_grupo'),
    path('<int:id>/', ver_grupo, name='ver_grupo'),
    path('editar/<int:id>/', editar_grupo, name='editar_grupo'),
    path('mis/', mis_grupos, name='mis_grupos'),
]