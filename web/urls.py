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
    path('contacto/', views.contacto, name='contacto'),
    path('carrito/', views.carrito, name='carrito'),
    path('registro/', views.registro, name='registro'),

    # Vista protegida solo para administradores
    path('gestion/usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('gestion/usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # Vistas protegidas por rol para CRUD de Juegos y Categorías
    path('gestion/juegos/', views.vista_juegos, name='vista_juegos'),
    path('gestion/categorias/', views.vista_categorias, name='vista_categorias'),

    # Ruta dinámica para las categorías
    path('categoria/<int:categoria_id>/', views.subcategoria, name='subcategoria'),

    # Ruta dinámica para juegos
    path('juego/<int:juego_id>/', views.detalle_juego, name='detalle_juego'),
]

