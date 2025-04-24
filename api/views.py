from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated  # seguridad de la api (interna)
from core.models import Categoria
from .serializers import CategoriaSerializer


from rest_framework.authentication import TokenAuthentication


# La vista de categorías solo será accesible para usuarios autenticados
@permission_classes([IsAuthenticated])
class CategoriaListAPIView(generics.ListAPIView):
    serializer_class = CategoriaSerializer
    # El permiso ya está definido en el decorador, no es necesario repetirlo aquí

    def get_queryset(self):
        queryset = Categoria.objects.all()
        nombre = self.request.query_params.get('nombre')
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        return queryset