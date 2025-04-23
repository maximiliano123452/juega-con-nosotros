from django.urls import path
from .views import CategoriaListAPIView

urlpatterns = [
    path('categorias/', CategoriaListAPIView.as_view(), name='api_categorias'),
]
