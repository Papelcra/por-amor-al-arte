from django.db import models
from django.conf import settings
from catalog.models import Genre

User = settings.AUTH_USER_MODEL

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=100)
    description = models.TextField()
    profile_image = models.ImageField(upload_to='artists/', null=True, blank=True)

    genres = models.ManyToManyField(Genre, blank=True)

    def __str__(self):
        return self.stage_name