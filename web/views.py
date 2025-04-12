from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import Categoria, Juego, Usuario
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password 
from django.utils import timezone
from datetime import datetime



# Vistas principales
def index(request):
    categorias = Categoria.objects.all()
    return render(request, 'web/index.html', {'categorias': categorias})

def login(request):
    return render(request, 'web/login.html')

# Vista para cargar el formulario de registro
def registro(request):
    return render(request, 'web/registro.html')


# Vista para manejar el registro via AJAX
def registro_ajax(request):
    if request.method == "POST" and request.is_ajax():
        try:
            nombre = request.POST.get('nombre_completo')
            usuario = request.POST.get('nombre_usuario')
            email = request.POST.get('correo_electronico')
            password = request.POST.get('contrasena')
            password_repetir = request.POST.get('repetir_contrasena')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            direccion = request.POST.get('direccion_despacho')
            rol = request.POST.get('rol')

            print(f"Datos recibidos: {nombre}, {usuario}, {email}, {password}, {fecha_nacimiento}, {direccion}, {rol}")

            # Validación de contraseñas
            if password != password_repetir:
                return JsonResponse({"success": False, "message": "Las contraseñas no coinciden"})

            # Validación de otros campos si es necesario
            if not nombre or not usuario or not email:
                return JsonResponse({"success": False, "message": "Todos los campos son obligatorios"})

            # Crear el usuario
            contrasena_encriptada = make_password(password)
            usuario = Usuario.objects.create(
                nombre_completo=nombre,
                nombre_usuario=usuario,
                correo_electronico=email,
                contrasena=contrasena_encriptada,
                fecha_nacimiento=fecha_nacimiento,
                direccion_despacho=direccion,
                rol=rol
            )
            # Si todo es correcto, responde con éxito
            return JsonResponse({"success": True, "message": "¡Registro exitoso! Ahora puedes iniciar sesión."})
        except Exception as e:
            # Si hay algún error, lo manejas aquí
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"})
    return JsonResponse({"success": False, "message": "Solicitud no válida."})


def perfil(request):
    return render(request, 'web/perfil.html')

def recuperar(request):
    return render(request, 'web/recuperar.html')

def contacto(request):
    return render(request, 'web/contacto.html')

def carrito(request):
    return render(request, 'web/carrito.html')

# Vistas por categoría (podrías eliminarlas si usas solo `subcategoria`)

def categoria_carreras(request):
    categoria = get_object_or_404(Categoria, nombre__iexact="Carreras")
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'categorias/carreras.html', {"categoria": categoria, "juegos": juegos})

def categoria_cozy(request):
    categoria = get_object_or_404(Categoria, nombre__iexact="Cozy")
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'categorias/cozy.html', {"categoria": categoria, "juegos": juegos})

def categoria_mundoabierto(request):
    categoria = get_object_or_404(Categoria, nombre__iexact="Mundo Abierto")
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'categorias/mundoabierto.html', {"categoria": categoria, "juegos": juegos})

def categoria_shooters(request):
    categoria = get_object_or_404(Categoria, nombre__iexact="Shooters")
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'categorias/shooters.html', {"categoria": categoria, "juegos": juegos})

def categoria_terror(request):
    categoria = get_object_or_404(Categoria, nombre__iexact="Terror")
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'categorias/terror.html', {"categoria": categoria, "juegos": juegos})

# Vista dinámica por ID
def subcategoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'web/subcategorias.html', {
        'categoria': categoria,
        'juegos': juegos
    })

# Detalle del juego
def detalle_juego(request, juego_id):
    juego = get_object_or_404(Juego, pk=juego_id)
    return render(request, 'web/detalle.html', {'juego': juego})
