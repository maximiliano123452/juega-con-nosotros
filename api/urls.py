from django.urls import path
from .views import CategoriaAPIView, CategoriaDetailAPIView, JuegoAPIView, JuegoDetailAPIView

from rest_framework.authtoken.views import obtain_auth_token
from .views_externa import juegos_populares, obtener_lanzamientos

urlpatterns = [
    path('juegos-populares/', juegos_populares, name='juegos_populares'),
    path('obtener_lanzamientos/', obtener_lanzamientos, name='obtener_lanzamientos'),
    path('categorias/', CategoriaAPIView.as_view(), name='categoria-list-create'),
    path('categorias/<int:pk>/', CategoriaDetailAPIView.as_view(), name='categoria-detail'),
    path('juegos/', JuegoAPIView.as_view(), name='juego-list-create'),
    path('juegos/<int:pk>/', JuegoDetailAPIView.as_view(), name='juego-detail'),
    path('token/', obtain_auth_token, name='api_token_auth'),
]
