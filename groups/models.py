# groups/models.py
from django.db import models
from django.conf import settings
from artists.models import Artist
from catalog.models import Genre

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    profile_image = models.ImageField(upload_to='groups/', null=True, blank=True)
    
    # Mantenemos esto si quieres que el ADMIN también pueda agregar gente manualmente
    members = models.ManyToManyField(
        Artist, 
        blank=True, 
        related_name='member_of_groups' # Cambiado para no chocar con el artist.group
    )
    genres = models.ManyToManyField(Genre, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name