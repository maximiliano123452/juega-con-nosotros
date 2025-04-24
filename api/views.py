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
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]  #  solo acceden los usuarios logueados 

@api_view(['GET'])
def juegos_populares(request):
    """Devuelve una lista de juegos populares desde la API RAWG"""
    juegos = obtener_juegos_populares()
    return Response(juegos)


