from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


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


class Favorito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario.nombre_usuario} - {self.juego.nombre}"

    class Meta:
        db_table = 'core_favorito'



class Contacto(models.Model):
    nombre = models.CharField('Nombre completo', max_length=100)
    email = models.EmailField('Correo electrónico')
    mensaje = models.TextField('Mensaje')
    fecha_creacion = models.DateTimeField('Fecha de envío', default=timezone.now)
    leido = models.BooleanField('¿Leído?', default=False)
    respuesta = models.TextField('Respuesta', blank=True, null=True)
    
    def __str__(self):
        return f"Mensaje de {self.nombre} ({self.email})"
    
    class Meta:
        verbose_name = 'Mensaje de contacto'
        verbose_name_plural = 'Mensajes de contacto'
        ordering = ['-fecha_creacion']


class Resena(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    juego = models.ForeignKey('Juego', on_delete=models.CASCADE)
    puntuacion = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Puntuación del 1 al 5"
    )
    comentario = models.TextField(max_length=500, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_resena'
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
        unique_together = ('usuario', 'juego')  # Un usuario solo puede reseñar un juego una vez

    def __str__(self):
        return f"Reseña de {self.usuario.nombre_usuario} para {self.juego.nombre} ({self.puntuacion}/5)"