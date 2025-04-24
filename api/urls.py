from django.urls import path
from .views import CategoriaListAPIView

from rest_framework.authtoken.views import obtain_auth_token
from .views_externa import juegos_populares

urlpatterns = [
    path('juegos-populares/', juegos_populares, name='juegos_populares'),
    path('categorias/', CategoriaListAPIView.as_view(), name='api_categorias'),
    path('token/', obtain_auth_token, name='api_token_auth'),
]
