from rest_framework import generics
from core.models import Categoria
from .serializers import CategoriaSerializer

class CategoriaListAPIView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

