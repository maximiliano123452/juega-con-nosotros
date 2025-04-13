from django.urls import path
from . import views

urlpatterns = [
    # Rutas principales
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('login/ajax/', views.login_ajax, name='login_ajax'),
    path('registro/ajax/', views.registro_ajax, name='registro_ajax'),
    path('perfil/', views.perfil, name='perfil'),
    path('recuperar/', views.recuperar, name='recuperar'),
    path('contacto/', views.contacto, name='contacto'),
    path('carrito/', views.carrito, name='carrito'),
    path('registro/', views.registro, name='registro'),
    
    # Ruta dinámica para las categorías
    path('categoria/<int:categoria_id>/', views.subcategoria, name='subcategoria'),
    
    # Ruta dinámica para juegos
    path('juego/<int:juego_id>/', views.detalle_juego, name='detalle_juego'),
]


