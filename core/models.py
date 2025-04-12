from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    lema = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen = models.CharField(max_length=255)  # Ruta relativa a la imagen en static/img

    def __str__(self):
        return self.titulo

class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=500)
    precio = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    plataformas = models.CharField(max_length=255, null=True, blank=True)
    imagen = models.CharField(max_length=255, null=True, blank=True)  # Permitir null y blank

    def __str__(self):
        return self.nombre