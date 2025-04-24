from django.urls import path
from .views import CategoriaListAPIView, juegos_populares
from rest_framework.authtoken.views import obtain_auth_token
from api.viewsLogin import login

urlpatterns = [
    path('categorias/', CategoriaListAPIView.as_view(), name='api_categorias'),
    path('juegos-populares/', juegos_populares, name='juegos_populares'),
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('login/', login, name='login'),
]
