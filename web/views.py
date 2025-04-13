from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import Categoria, Juego, Usuario
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from datetime import datetime
from core.forms import UsuarioForm, LoginForm

# Vistas principales
def index(request):
    categorias = Categoria.objects.all()
    usuario_nombre = None
    if request.session.get('usuario_id'):
        try:
            usuario = Usuario.objects.get(id=request.session['usuario_id'])
            usuario_nombre = usuario.nombre_usuario
        except Usuario.DoesNotExist:
            pass

    return render(request, 'web/index.html', {
        'categorias': categorias,
        'usuario_nombre': usuario_nombre
    })

# Vista de formulario de inicio de sesión
def login(request):
    form = LoginForm()  # Crear una instancia del formulario
    return render(request, 'web/login.html', {'form': form})

# Vista para manejar el formulario de inicio de sesión via AJAX
def login_ajax(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo_electronico']
            contrasena = form.cleaned_data['contrasena']
            try:
                usuario = Usuario.objects.get(correo_electronico=correo)
                if check_password(contrasena, usuario.contrasena):
                    request.session['usuario_id'] = usuario.id
                    return JsonResponse({'success': True, 'message': 'Inicio de Sesión Exitoso, redirigiendo al perfil'})
                else:
                    return JsonResponse({'success': False, 'error': 'Contraseña incorrecta'})
            except Usuario.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Usuario no encontrado'})
        else:
            return JsonResponse({'success': False, 'error': 'Datos del formulario inválidos'})
    return JsonResponse({'success': False, 'error': 'Método inválido'})

# Vista de formulario de registro
def registro(request):
    form = UsuarioForm()
    return render(request, 'web/registro.html', {'form': form})

# Vista para el formulario de registro
def formulario_registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UsuarioForm()
    return render(request, 'registro.html', {'form': form})

# Vista para manejar el formulario de registro via AJAX
def registro_ajax(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Registro Exitoso, redirigiendo al inicio de sesión.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def perfil(request):
    return render(request, 'web/perfil.html')

def recuperar(request):
    return render(request, 'web/recuperar.html')

def contacto(request):
    return render(request, 'web/contacto.html')

def carrito(request):
    return render(request, 'web/carrito.html')

# Vista de administración solo para el rol administrador
def admin_usuarios(request):
    if not request.session.get('usuario_id'):
        return redirect('login')

    usuario_actual = Usuario.objects.get(id=request.session['usuario_id'])

    if usuario_actual.rol != 'administrador':
        return render(request, 'web/error_permiso.html', status=403)

    usuarios = Usuario.objects.all()
    return render(request, 'web/admin_usuarios.html', {'usuarios': usuarios})

# Vistas por categoría 
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
