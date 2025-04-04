from django.urls import path
from . import views

urlpatterns = [
    # Rutas principales
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
    path('recuperar/', views.recuperar, name='recuperar'),
    path('contacto/', views.contacto, name='contacto'),
    path('carrito/', views.carrito, name='carrito'),

    # Rutas para las categorías
    path('categorias/carreras/', views.categoria_carreras, name='categoria_carreras'),
    path('categorias/cozy/', views.categoria_cozy, name='categoria_cozy'),
    path('categorias/mundo_abierto/', views.categoria_mundoabierto, name='categoria_mundoabierto'),
    path('categorias/shooters/', views.categoria_shooters, name='categoria_shooters'), 
    path('categorias/terror/', views.categoria_terror, name='categoria_terror'),

    # Rutas para los juegos - Carreras
    path('juegos/carreras/crashteamracing/', views.crashteamracing, name='crashteamracing'),
    path('juegos/carreras/mariokart8deluxe/', views.mariokart8deluxe, name='mariokart8deluxe'),

    # Juegos - Cozy
    path('juegos/cozy/stardewvalley/', views.stardewvalley, name='stardewvalley'),
    path('juegos/cozy/spiritfarer/', views.spiritfarer, name='spiritfarer'),

    # Juegos - Mundo Abierto
    path('juegos/mundoabierto/cyberpunk2077/', views.cyberpunk2077, name='cyberpunk2077'),
    path('juegos/mundoabierto/zeldatotk/', views.zeldatotk, name='zeldatotk'),

    # Juegos - Shooters
    path('juegos/shooters/doometernal/', views.doometernal, name='doometernal'),
    path('juegos/shooters/splatoon2/', views.splatoon2, name='splatoon2'),

    # Juegos - Terror
    path('juegos/terror/alanwake2/', views.alanwake2, name='alanwake2'),
    path('juegos/terror/residentevil4remake/', views.residentevil4remake, name='residentevil4remake'),
]

