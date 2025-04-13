from django.shortcuts import render, get_object_or_404, redirect
from core.models import Categoria, Juego, Usuario
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from core.forms import UsuarioForm, LoginForm
from django.contrib.auth import logout



# Función obtener nombre usuario
def obtener_usuario_nombre(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            return usuario.nombre_usuario
        except Usuario.DoesNotExist:
            return None
    return None

# Vistas principales
def index(request):
    categorias = Categoria.objects.all()
    return render(request, 'web/index.html', {
        'categorias': categorias,
        'usuario_nombre': obtener_usuario_nombre(request)
    })

# Vista de formulario de inicio de sesión
def login(request):
    form = LoginForm()
    return render(request, 'web/login.html', {
        'form': form,
        'usuario_nombre': obtener_usuario_nombre(request)
    })

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
                    return JsonResponse({'success': True, 'message': 'Inicio de Sesión Exitoso, redirigiendo al inicio'})
                else:
                    return JsonResponse({'success': False, 'error': 'Contraseña incorrecta'})
            except Usuario.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Usuario no encontrado'})
        else:
            return JsonResponse({'success': False, 'error': 'Datos del formulario inválidos'})
    return JsonResponse({'success': False, 'error': 'Método inválido'})


# Vista para manejar el Cierre de sesión
def cerrar_sesion(request):
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
    return redirect('index')


# Vista de formulario de registro
def registro(request):
    form = UsuarioForm()
    return render(request, 'web/registro.html', {
        'form': form,
        'usuario_nombre': obtener_usuario_nombre(request)
    })


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
def contacto(request):
    return render(request, 'web/contacto.html', {
        'usuario_nombre': obtener_usuario_nombre(request)
    })

def carrito(request):
    return render(request, 'web/carrito.html', {
        'usuario_nombre': obtener_usuario_nombre(request)
    })

def perfil(request):
    usuario_nombre = obtener_usuario_nombre(request)
    if not usuario_nombre:
        return redirect('login')

    return render(request, 'web/perfil.html', {
        'usuario_nombre': usuario_nombre
    })

def recuperar(request):
    return render(request, 'web/recuperar.html', {
        'usuario_nombre': obtener_usuario_nombre(request)
    })


# Vistas por categoría 
def categoria_carreras(request):
    categoria = get_object_or_404(Categoria, nombre__iexact="Carreras")
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'categorias/carreras.html', {
        "categoria": categoria,
        "juegos": juegos,
        'usuario_nombre': obtener_usuario_nombre(request)
    })

# Vistas para cada categoría
def categoria_cozy(request):
    categoria = get_object_or_404(Categoria, nombre__iexact="Cozy")
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'categorias/cozy.html', {
        "categoria": categoria,
        "juegos": juegos,
        'usuario_nombre': obtener_usuario_nombre(request)
    })

def categoria_mundoabierto(request):
    categoria = get_object_or_404(Categoria, nombre__iexact="Mundo Abierto")
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'categorias/mundoabierto.html', {
        "categoria": categoria,
        "juegos": juegos,
        'usuario_nombre': obtener_usuario_nombre(request)
    })

def categoria_shooters(request):
    categoria = get_object_or_404(Categoria, nombre__iexact="Shooters")
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'categorias/shooters.html', {
        "categoria": categoria,
        "juegos": juegos,
        'usuario_nombre': obtener_usuario_nombre(request)
    })

def categoria_terror(request):
    categoria = get_object_or_404(Categoria, nombre__iexact="Terror")
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'categorias/terror.html', {
        "categoria": categoria,
        "juegos": juegos,
        'usuario_nombre': obtener_usuario_nombre(request)
    })


# Vista dinámica por ID
def subcategoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'web/subcategorias.html', {
        'categoria': categoria,
        'juegos': juegos,
        'usuario_nombre': obtener_usuario_nombre(request)
    })

# Detalle del juego
def detalle_juego(request, juego_id):
    juego = get_object_or_404(Juego, pk=juego_id)
    return render(request, 'web/detalle.html', {
        'juego': juego,
        'usuario_nombre': obtener_usuario_nombre(request)
    })
