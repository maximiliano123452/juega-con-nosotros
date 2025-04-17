from django.urls import path
from . import views

urlpatterns = [
    # Rutas principales
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('login/ajax/', views.login_ajax, name='login_ajax'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('registro/ajax/', views.registro_ajax, name='registro_ajax'),
    path('perfil/', views.perfil, name='perfil'),
    path('recuperar/', views.recuperar, name='recuperar'),
    path('recuperar_ajax/', views.recuperar_ajax, name='recuperar_ajax'),
    path('contacto/', views.contacto, name='contacto'),
    path('carrito/', views.carrito, name='carrito'),
    path('registro/', views.registro, name='registro'),
    path('agregar_juego/', views.agregar_juego, name='agregar_juego'),
    path('editar_usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),

    # Vista protegida solo para administradores
    path('gestion/usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('gestion/usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # Ruta para gestión de categorias
    path('categoria/gestion/', views.categoria_gestion, name='categoria_gestion'),

    # Rutas para la gestión de juegos
    path('juego/gestion/', views.juego_gestion, name='juego_gestion'), 
    path('juego/gestion/editar/<int:id>/', views.editar_juego, name='editar_juego'),  # Ruta para editar juegos
    path('juego/gestion/eliminar/<int:id>/', views.eliminar_juego, name='eliminar_juego'),  # Ruta para eliminar juegos


    # Ruta dinámica para las categorías
    path('categoria/<int:categoria_id>/', views.subcategoria, name='subcategoria'),

    # Ruta dinámica para juegos
    path('juego/<int:juego_id>/', views.detalle_juego, name='detalle_juego'),

]

