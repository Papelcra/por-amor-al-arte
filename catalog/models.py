from django.db import models

class LineaArtistica(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Línea Artística"
        verbose_name_plural = "Líneas Artísticas"


class Genre(models.Model):
    nombre = models.CharField(max_length=100)
    linea = models.ForeignKey(LineaArtistica, on_delete=models.CASCADE, related_name='generos')

    def __str__(self):
        return f"{self.nombre} ({self.linea.nombre})"