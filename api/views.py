from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated  # seguridad de la api (interna)
from core.models import Categoria
from .serializers import CategoriaSerializer
from .external import obtener_juegos_populares

from rest_framework.authentication import TokenAuthentication


@permission_classes([IsAuthenticated])
class CategoriaListAPIView(generics.ListAPIView):
    
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]  #  solo acceden los usuarios logueados 

    def get_queryset(self):
        queryset = Categoria.objects.all()
        nombre = self.request.query_params.get('nombre')
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        return queryset

@api_view(['GET'])
def juegos_populares(request):
    """Devuelve una lista de juegos populares desde la API RAWG"""
    juegos = obtener_juegos_populares()
    return Response(juegos)


