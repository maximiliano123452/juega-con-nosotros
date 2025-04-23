from django.urls import path
from .views import CategoriaListAPIView, juegos_populares

urlpatterns = [
    path('categorias/', CategoriaListAPIView.as_view(), name='api_categorias'),
    path('juegos-populares/', juegos_populares, name='juegos_populares'),
]
