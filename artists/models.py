from django.db import models
from django.conf import settings
from catalog.models import Genre, LineaArtistica 
from django.db import models
from django.contrib.auth.models import User

User = settings.AUTH_USER_MODEL

# artists/models.py
class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='artists/', blank=True, null=True)
    
    linea = models.ForeignKey('catalog.LineaArtistica', on_delete=models.SET_NULL, null=True, blank=True)
    
    # ← ESTO ES LO MÁS IMPORTANTE
    group = models.ForeignKey(
        'groups.Group',                    # ← Usa string si está en otra app
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='artists'             # ← Muy recomendado
    )

    genres = models.ManyToManyField('catalog.Genre', blank=True)

    def __str__(self):
        return self.stage_name

# ── NUEVO ──
class ArtistImage(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='artists/gallery/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Imagen de {self.artist.stage_name}"