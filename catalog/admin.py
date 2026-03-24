from django.contrib import admin
from .models import LineaArtistica, Genre

@admin.register(LineaArtistica)
class LineaArtisticaAdmin(admin.ModelAdmin):  # <-- Antes decía admin.admin.ModelAdmin
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):           # <-- Antes decía admin.admin.ModelAdmin
    list_display = ('nombre', 'linea')
    list_filter = ('linea',)
    search_fields = ('nombre',)