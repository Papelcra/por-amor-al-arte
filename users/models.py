from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('artist', 'Artista'),
        ('group_admin', 'Administrador de Agrupación'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # opcional pero útil
    profile_image = models.ImageField(upload_to='users/', null=True, blank=True)

    def __str__(self):
        return self.username