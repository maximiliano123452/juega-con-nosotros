from rest_framework.decorators import api_view
from rest_framework.response import Response
from .external import obtener_juegos_populares
import requests
from django.shortcuts import render
from datetime import datetime

#API externa de RAWG para juegos populares
@api_view(['GET'])
def juegos_populares(request):
    """Devuelve una lista de juegos populares desde la API RAWG"""
    juegos = obtener_juegos_populares()
    return Response(juegos)


#API externa de twitch para lanzamientos de juegos 
def obtener_lanzamientos():
    client_id = 'op7e9vi3fvjduvjvewxccy1w32svbp'
    access_token = 'eu6fqmesizyw35p2m9dbdgvuhbd0tp'

    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'text/plain'
    }

    body = '''
        fields name, first_release_date, platforms.name, cover.url;
        where first_release_date > 1714400000;
        sort first_release_date asc;
        limit 15;
    '''

    response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=body)
    juegos_crudos = response.json() if response.status_code == 200 else []
    lanzamientos = []

    for juego in juegos_crudos:
        timestamp = juego.get('first_release_date')
        fecha = datetime.utcfromtimestamp(timestamp).strftime('%d/%m/%Y') if timestamp else 'Sin fecha'
        lanzamientos.append({
            'nombre': juego.get('name')[:20],  # Limita el nombre a 20 caracteres
            'fecha': fecha,
            'imagen': juego.get('cover', {}).get('url')
        })

    return lanzamientos