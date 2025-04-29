import requests
from decouple import config

def obtener_juegos_populares():
    """Consulta la API de RAWG para traer los juegos populares"""
    api_key = config("RAWG_API_KEY")
    url = f"https://api.rawg.io/api/games?key={api_key}&ordering=-rating&page_size=5"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.RequestException as e:
        print(f"Error al conectar con RAWG: {e}")
        return []


