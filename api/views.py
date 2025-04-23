from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Categoria
from .serializers import CategoriaSerializer
from .external import obtener_juegos_populares

class CategoriaListAPIView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

@api_view(['GET'])
def juegos_populares(request):
    """Devuelve una lista de juegos populares desde la API RAWG"""
    juegos = obtener_juegos_populares()
    return Response(juegos)


