from django.db import models
from artists.models import Artist
from catalog.models import Genre

from django.conf import settings

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    profile_image = models.ImageField(upload_to='groups/', null=True, blank=True)

    members = models.ManyToManyField(
    Artist,
    blank=True,
    related_name='groups'
    )
    genres = models.ManyToManyField(Genre, blank=True)

    # 🔥 CLAVE
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name