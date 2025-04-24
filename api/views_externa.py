from rest_framework.decorators import api_view
from rest_framework.response import Response
from .external import obtener_juegos_populares

@api_view(['GET'])
def juegos_populares(request):
    """Devuelve una lista de juegos populares desde la API RAWG"""
    juegos = obtener_juegos_populares()
    return Response(juegos)