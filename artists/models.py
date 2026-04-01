from django.db import models
from django.conf import settings
from catalog.models import Genre

User = settings.AUTH_USER_MODEL

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=100)
    description = models.TextField()
    profile_image = models.ImageField(upload_to='artists/', null=True, blank=True)
    genres = models.ManyToManyField(Genre)

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