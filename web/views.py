from django.shortcuts import render, get_object_or_404, redirect
from core.models import Categoria, Juego, Usuario
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from core.forms import UsuarioForm, LoginForm, PerfilForm, JuegoForm
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


# para obtener datos del usuario logueado
def obtener_usuario_nombre(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            return {
                'usuario_nombre': usuario.nombre_usuario,
                'usuario_rol': usuario.rol
            }
        except Usuario.DoesNotExist:
            return {
                'usuario_nombre': None,
                'usuario_rol': None
            }
    return {
        'usuario_nombre': None,
        'usuario_rol': None
    }

# Vistas generales
def index(request):
    categorias = Categoria.objects.all()
    datos_usuario = obtener_usuario_nombre(request)
    return render(request, 'web/index.html', {'categorias': categorias, **datos_usuario})

def login(request):
    form = LoginForm()
    datos_usuario = obtener_usuario_nombre(request)
    return render(request, 'web/login.html', {'form': form, **datos_usuario})

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

def cerrar_sesion(request):
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
    return redirect('index')

def registro(request):
    form = UsuarioForm()
    datos_usuario = obtener_usuario_nombre(request)
    return render(request, 'web/registro.html', {'form': form, **datos_usuario})

def formulario_registro(request):
    form = UsuarioForm(request.POST or None)
    datos_usuario = obtener_usuario_nombre(request)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'registro.html', {'form': form, **datos_usuario})

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
    return render(request, 'web/contacto.html', obtener_usuario_nombre(request))

def carrito(request):
    return render(request, 'web/carrito.html', obtener_usuario_nombre(request))

def perfil(request):
    usuario_nombre = obtener_usuario_nombre(request)
    if not usuario_nombre:
        return redirect('login')
    usuario = Usuario.objects.get(id=request.session['usuario_id'])
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario_modificado = form.save(commit=False)
            nueva_contrasena = form.cleaned_data.get('contrasena')
            if nueva_contrasena:
                usuario_modificado.contrasena = make_password(nueva_contrasena)
            usuario_modificado.save()
            messages.success(request, '✅ Tus datos se han actualizado correctamente.')
        else:
            messages.error(request, '❌ Hubo errores al actualizar tus datos. Por favor revisa el formulario.')
    else:
        form = PerfilForm(instance=usuario)
    return render(request, 'web/perfil.html', {
        'usuario_nombre': usuario.nombre_usuario,
        'usuario_rol': usuario.rol,
        'usuario': usuario,
        'form': form
    }) 

def recuperar(request):
    return render(request, 'web/recuperar.html', obtener_usuario_nombre(request))

# Vista para mostrar usuarios
def admin_usuarios(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
    usuario_actual = Usuario.objects.get(id=request.session['usuario_id'])
    if usuario_actual.rol != 'administrador':
        return render(request, 'web/error_permiso.html', status=403)
    usuarios = Usuario.objects.exclude(id=usuario_actual.id)
    return render(request, 'web/admin_usuarios.html', {
        'usuarios': usuarios,
        **obtener_usuario_nombre(request)
    })

# Vista para eliminar usuario
@csrf_exempt
def eliminar_usuario(request, usuario_id):
    if request.method == 'POST':
        usuario_actual = Usuario.objects.get(id=request.session.get('usuario_id'))
        if usuario_actual.rol == 'administrador':
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                usuario.delete()
            except Usuario.DoesNotExist:
                pass
    return redirect('admin_usuarios')

# Vista para editar usuario
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('admin_usuarios')  # Redirige de nuevo a la lista de usuarios
    else:
        form = UsuarioForm(instance=usuario)
    
    return render(request, 'web/editar_usuario.html', {'form': form, 'usuario': usuario, **obtener_usuario_nombre(request)})



# Vistas de juegos y categorias protegidas por rol
#def vista_juegos(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    usuario = Usuario.objects.get(id=usuario_id)
    if usuario.rol not in ['administrador', 'vendedor']:
        return render(request, 'web/error_permiso.html', status=403)
    juegos = Juego.objects.select_related('categoria').all()
    return render(request, 'web/juegos.html', {
        'juegos': juegos,
        **obtener_usuario_nombre(request)
    })

#def vista_categorias(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    usuario = Usuario.objects.get(id=usuario_id)
    if usuario.rol not in ['administrador', 'vendedor']:
        return render(request, 'web/error_permiso.html', status=403)
    categorias = Categoria.objects.all()
    return render(request, 'web/categorias.html', {
        'categorias': categorias,
        **obtener_usuario_nombre(request)
    })

# Categorias individuales
def categoria_carreras(request):
    categoria = get_object_or_404(Categoria, nombre__iexact="Carreras")
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'categorias/carreras.html', {'categoria': categoria, 'juegos': juegos, **obtener_usuario_nombre(request)})

def categoria_cozy(request):
    categoria = get_object_or_404(Categoria, nombre__iexact="Cozy")
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'categorias/cozy.html', {'categoria': categoria, 'juegos': juegos, **obtener_usuario_nombre(request)})

def categoria_mundoabierto(request):
    categoria = get_object_or_404(Categoria, nombre__iexact="Mundo Abierto")
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'categorias/mundoabierto.html', {'categoria': categoria, 'juegos': juegos, **obtener_usuario_nombre(request)})

def categoria_shooters(request):
    categoria = get_object_or_404(Categoria, nombre__iexact="Shooters")
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'categorias/shooters.html', {'categoria': categoria, 'juegos': juegos, **obtener_usuario_nombre(request)})

def categoria_terror(request):
    categoria = get_object_or_404(Categoria, nombre__iexact="Terror")
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'categorias/terror.html', {'categoria': categoria, 'juegos': juegos, **obtener_usuario_nombre(request)})

def subcategoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    juegos = Juego.objects.filter(categoria=categoria)
    return render(request, 'web/subcategorias.html', {'categoria': categoria, 'juegos': juegos, **obtener_usuario_nombre(request)})

def detalle_juego(request, juego_id):
    juego = get_object_or_404(Juego, pk=juego_id)
    return render(request, 'web/detalle.html', {'juego': juego, **obtener_usuario_nombre(request)})



# Vista para agregar juego
def agregar_juego(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)
    if usuario.rol not in ['administrador', 'vendedor']:
        return render(request, 'web/error_permiso.html', status=403)

    if request.method == 'POST':
        form = JuegoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vista_juegos')
    else:
        form = JuegoForm()

    return render(request, 'web/agregar_juego.html', {
        'form': form,
        **obtener_usuario_nombre(request)
    })




def juego_gestion(request):
    juegos = Juego.objects.all()  # Obtener todos los juegos registrados
    return render(request, 'web/juego_gestion.html', {'juegos': juegos, **obtener_usuario_nombre(request)})

# Vista para editar un juego
def editar_juego(request, id):
    juego = get_object_or_404(Juego, id=id)  # Trae el juego por su id
    if request.method == 'POST':
        form = JuegoForm(request.POST, instance=juego)  # Suponiendo que tienes un formulario de juego
        if form.is_valid():
            form.save()  # Guarda los cambios
            messages.success(request, 'Juego modificado con éxito.')
            return redirect('web/juego_gestion.html')
    else:
        form = JuegoForm(instance=juego)
    return render(request, 'web/editar_juego.html', {'form': form, 'juego': juego, **obtener_usuario_nombre(request)})

def eliminar_juego(request, id):
    juego = get_object_or_404(Juego, id=id)
    if request.method == 'POST':
        # No eliminamos el juego, solo mostramos un mensaje de error
        # No se eliminan juegos por ahora ya que influye en el diseño básico de la web
        messages.error(request, 'Error: No se puede eliminar el juego. Operación desactivada temporalmente.')
        return redirect('juego_gestion')  # Redirige de nuevo a la página de gestión de juegos

    return render(request, 'web/confirm_eliminar_juego.html', {'juego': juego, **obtener_usuario_nombre(request)})