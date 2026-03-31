from django.urls import path
from .views import crear_grupo, lista_grupos,ver_grupo,editar_grupo,mis_grupos

app_name = 'groups'

urlpatterns = [
    path('', lista_grupos, name='lista_grupos'),  # 👈 ESTA FALTABA
    path('crear/', crear_grupo, name='crear_grupo'),
    path('<int:group_id>/', ver_grupo, name='ver_grupo'),
    path('editar/<int:group_id>/', editar_grupo, name='editar_grupo'),
    path('mis/', mis_grupos, name='mis_grupos'),
]