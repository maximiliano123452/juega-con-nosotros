from django.shortcuts import render, get_object_or_404, redirect
from core.models import Categoria, Juego, Usuario, Contacto, Resena
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from core.forms import UsuarioForm, LoginForm, PerfilForm, JuegoForm, ResenaForm
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json, requests
from api.views_externa import obtener_lanzamientos
from django.db import models

# Decorador para proteger vistas según el rol del usuario
def solo_rol_permitido(roles=[]):
    def decorador(funcion):
        def wrapper(request, *args, **kwargs):
            usuario_id = request.session.get('usuario_id')
            if not usuario_id:
                return redirect('login')

            usuario = Usuario.objects.get(id=usuario_id)

            if usuario.rol in roles:
                return funcion(request, *args, **kwargs)
            else:
                datos_usuario = obtener_usuario_nombre(request)
                return render(request, 'web/error_permiso.html', context=datos_usuario, status=403)

        return wrapper
    return decorador


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
    
    # Llamar a la API de RAWG
    url = "https://api.rawg.io/api/games"
    params = {
        'key': 'b5009a1140ad4ea68365396fed2e19ef',
        'page_size': 5,
        'ordering': '-added'
    }

    games = []
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Esto lanza una excepción si el código de estado no es 200
        if response.status_code == 200:
            data = response.json()
            for game in data.get('results', []):
                # Verificar si rating existe y convertirlo a formato adecuado
                rating = game.get('rating')
                if rating:
                    rating = str(rating).replace(',', '.')  # Asegurarse de que el rating se maneje correctamente
                else:
                    rating = 'No disponible'

                games.append({
                    'nombre': game.get('name'),
                    'rating': rating,
                    'imagen': game.get('background_image')
                })
    except requests.exceptions.RequestException as e:
        print("Error al obtener juegos populares:", e)
        games = []  # En caso de error, no se muestran juegos populares
    except Exception as e:
        print("Error inesperado:", e)
        games = []

    # Renderizar la plantilla con todo el contexto
    return render(request, 'web/index.html', {
        'categorias': categorias,
        'games': games,
        **datos_usuario
    })

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

@solo_rol_permitido(roles=['cliente', 'vendedor', 'administrador'])
def perfil(request):
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

def recuperar_ajax(request):
    if request.method == 'POST':
        print("✅ Vista recuperar_ajax fue llamada")
        datos = json.loads(request.body)
        correo = datos.get('correo')
        print(f"""
                📨 Simulación de correo enviado:

                Para: {correo}

                Instrucciones para recuperar contraseña.

                Juega con Nosotros
                """)
        return JsonResponse({'mensaje': 'Correo procesado'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@solo_rol_permitido(roles=['administrador'])
def admin_usuarios(request):
    usuario_actual = Usuario.objects.get(id=request.session['usuario_id'])
    usuarios = Usuario.objects.exclude(id=usuario_actual.id)
    return render(request, 'web/admin_usuarios.html', {
        'usuarios': usuarios,
        **obtener_usuario_nombre(request)
    })

@csrf_exempt
@solo_rol_permitido(roles=['administrador'])
def eliminar_usuario(request, usuario_id):
    if request.method == 'POST':
        usuario = Usuario.objects.get(id=request.session.get('usuario_id'))
        if usuario.rol == 'administrador':
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                usuario.delete()
            except Usuario.DoesNotExist:
                pass
    return redirect('admin_usuarios')

@solo_rol_permitido(roles=['administrador'])
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('admin_usuarios')
    else:
        form = PerfilForm(instance=usuario)

    return render(request, 'web/editar_usuario.html', {
        'form': form,
        'usuario': usuario,
        **obtener_usuario_nombre(request)
    })

@solo_rol_permitido(roles=['administrador', 'vendedor'])
def agregar_juego(request):
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

@solo_rol_permitido(roles=['administrador', 'vendedor'])
def juego_gestion(request):
    juegos = Juego.objects.all()
    return render(request, 'web/juego_gestion.html', {'juegos': juegos, **obtener_usuario_nombre(request)})

@solo_rol_permitido(roles=['administrador', 'vendedor'])
def editar_juego(request, id):
    juego = get_object_or_404(Juego, id=id)
    if request.method == 'POST':
        form = JuegoForm(request.POST, instance=juego)
        if form.is_valid():
            form.save()
            messages.success(request, 'Juego modificado con éxito.')
            return redirect('juego_gestion')
    else:
        form = JuegoForm(instance=juego)
    return render(request, 'web/editar_juego.html', {'form': form, 'juego': juego, **obtener_usuario_nombre(request)})

@solo_rol_permitido(roles=['administrador'])
def eliminar_juego(request, id):
    juego = get_object_or_404(Juego, id=id)
    if request.method == 'POST':
        messages.error(request, 'Error: No se puede eliminar el juego. Operación desactivada temporalmente.')
        return redirect('juego_gestion')
    return render(request, 'web/confirm_eliminar_juego.html', {'juego': juego, **obtener_usuario_nombre(request)})

@solo_rol_permitido(roles=['administrador', 'vendedor'])
def categoria_gestion(request):
    categorias = Categoria.objects.all()
    return render(request, 'web/categoria_gestion.html', {
        'categorias': categorias,
        **obtener_usuario_nombre(request)
    })

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


def lanzamientos(request):
    juegos_lanzamiento = obtener_lanzamientos()
    return render(request, 'web/lanzamientos.html', {
        'lanzamientos': juegos_lanzamiento,
        **obtener_usuario_nombre(request)
    })


def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        
        Contacto.objects.create(
            nombre=nombre,
            email=email,
            mensaje=mensaje
        )
        
        messages.success(request, '¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.')
        return redirect('contacto')
    
    return render(request, 'web/contacto.html', obtener_usuario_nombre(request))


def detalle_juego(request, juego_id):
    juego = get_object_or_404(Juego, pk=juego_id)
    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(id=usuario_id) if usuario_id else None
    
    # Obtener reseñas existentes
    reseñas = Resena.objects.filter(juego=juego).order_by('-fecha_creacion')
    
    # Manejar envío de nueva reseña
    if request.method == 'POST' and usuario:
        form = ResenaForm(request.POST)
        if form.is_valid():
            # Verificar si ya existe una reseña de este usuario
            reseña, created = Resena.objects.get_or_create(
                usuario=usuario,
                juego=juego,
                defaults=form.cleaned_data
            )
            if not created:
                # Actualizar reseña existente
                reseña.puntuacion = form.cleaned_data['puntuacion']
                reseña.comentario = form.cleaned_data['comentario']
                reseña.save()
            return redirect('detalle_juego', juego_id=juego.id)
    else:
        form = ResenaForm()
    
    # Calcular promedio de puntuaciones
    promedio = reseñas.aggregate(models.Avg('puntuacion'))['puntuacion__avg'] or 0
    
    context = {
        'juego': juego,
        'reseñas': reseñas,
        'form': form,
        'promedio': round(promedio, 1),
        'usuario_tiene_reseña': reseñas.filter(usuario=usuario).exists() if usuario else False,
        **obtener_usuario_nombre(request)
    }
    return render(request, 'web/detalle.html', context)