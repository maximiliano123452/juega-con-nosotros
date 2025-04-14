from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    lema = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen = models.CharField(max_length=255)  # Ruta relativa a la imagen en static/img

    def __str__(self):
        return self.titulo
    
    class Meta:
        db_table = 'core_categoria'

class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    plataformas = models.CharField(max_length=255, null=True, blank=True)
    imagen = models.CharField(max_length=255, null=True, blank=True)  # Permitir null y blank

    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'core_juego'

class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=200)
    nombre_usuario = models.CharField(max_length=50, unique=True)
    correo_electronico = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    direccion_despacho = models.CharField(max_length=255, null=True, blank=True)
    rol = models.CharField(max_length=20, choices=[
        ('administrador', 'Administrador'),
        ('vendedor', 'Vendedor'),
        ('cliente', 'Cliente'),
        ('invitado', 'Invitado'),
    ], default='invitado')

    def __str__(self):
        return self.nombre_usuario

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'core_usuario'