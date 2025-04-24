# Prototipo Tienda Videojuegos

Configuración:

1. Extraer wallet_g4db.zip en la raíz del proyecto y modificar archivo sqlnet.ora agregando tu ruta hacia "wallet_g4db" en DIRECTORY

Ejemplo:

WALLET_LOCATION = (SOURCE = (METHOD = file) (METHOD_DATA = (DIRECTORY = C:\tu\ruta\juega-con-nosotros\wallet_g4db)))
SSL_SERVER_DN_MATCH=yes

Utilizando terminal de VS Code:

2. Crear/Activar entorno virtual: python -m venv venv

Windows (PowerShell):
	.\venv\Scripts\Activate.ps1

MacOS (zsh):
	source venv/bin/activate

3. Añadir variable de entorno, modifica tu ruta hacia Oracle Instant Client
('C:tu\ruta\oracle\instantclient_23_7' o "/usr/tu/ruta/instantclient-basic")

Windows (PowerShell):
	[System.Environment]::SetEnvironmentVariable('ORACLE_CLIENT_PATH','C:tu\ruta\oracle\instantclient_23_7',[System.EnvironmentVariableTarget]::User)

MacOS (zsh):
	echo 'export ORACLE_CLIENT_PATH="/usr/tu/ruta/instantclient-basic"' >> ~/.zshrc
	echo 'export DYLD_LIBRARY_PATH="/usr/tu/ruta/instantclient-basic"' >> ~/.zshrc
	source ~/.zshrc

4. instalar dependencias

	pip install -r requirements.txt

5. Crear .env basado en el ejemplo

Windows (PowerShell):
	Copy-Item .env-ejemplo .env

MacOS (zsh):
	cp .env-ejemplo .env

6. Edita archivo .env con tus credenciales (en este caso estamos compartiendo todos el mismo usuario)

7. Ejecutar el proyecto

	python manage.py migrate core --fake

	python manage.py createsuperuser (opcional)

	python manage.py runserver





Integración de API REST y Consumo de API Externa RAWG 

	              parte 1: API REST interna (categorias del sistema)
 creacion de una API REST en Django para exponer los datos de la tabla Categoria de nuestra base de datos Oracle.

       Pasos realizados:
1. creacion de la app api:
python manage.py startapp api

2. registrar la app api y rest_framework en settings.py dentro de INSTALLED_APPS.

3. crear el archivo serializers.py dentro de la carpeta api con el siguiente contenido:
from rest_framework import serializers
from core.models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

4. agregar la vista en api/views.py:
from rest_framework import generics
from core.models import Categoria
from .serializers import CategoriaSerializer

class CategoriaListAPIView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

5.	crear api/urls.py con la siguiente ruta:
from django.urls import path
from .views import CategoriaListAPIView

urlpatterns = [
    path('categorias/', CategoriaListAPIView.as_view(), name='api_categorias'),
]

6. agregar la ruta en tienda_juegos/urls.py:
path('api/', include('api.urls')),  # Ruta para API REST


6.1 Se ha agregado seguridad por medio de token para la API Interna Categorias
    Para conseguir el token, hay que tener un superuser creado en django.
    
    En ARC:
        POST: http://127.0.0.1:8000/api/token/ 
        Headers: Content-Type     Application/json

        Body:
            {
            "username": "superuser",
            "password": "contraseñasuperuser"
            }
    
    Enviar: Esto generará el token.

Para usar el token:
    
	En ARC:
    	
	GET:  http://127.0.0.1:8000/api/categorias/
 	Headers: Authorization
	Value: Token pegartokenaquí
	Enviar: Devuelve un JSON con todas las categorias de la base de datos. 



Parte 2: Consumo de API externa (RAWG Video Games) 
	 integramos una API externa gratuita de videojuegos para traer juegos populares actuales al sistema.
	 ¿que hicimos?
1. nos registramos en RAWG.io
y copiamos la API Key gratuita:
ejemplo: b5009a1140ad4ea68365396fed2e19ef

2. agregar la clave al archivo .env:
RAWG_API_KEY=b5009a1140ad4ea68365396fed2e19ef

3. Crear un archivo llamado external.py en la app api con el siguiente codigo:

import requests
from decouple import config

def obtener_juegos_populares():
    API_KEY = config('RAWG_API_KEY')
    url = f'https://api.rawg.io/api/games?key={API_KEY}&page_size=5'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        juegos = []

        for juego in data.get('results', []):
            juegos.append({
                'nombre': juego['name'],
                'imagen': juego['background_image'],
                'rating': juego['rating'],
                'plataformas': [p['platform']['name'] for p in juego['platforms']],
            })
        return juegos
    return []
  
  4. editar views.py para agregar la vista que consume RAWG:
 
  from rest_framework.views import APIView
from rest_framework.response import Response
from .external import obtener_juegos_populares

class JuegosPopularesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        juegos = obtener_juegos_populares()
        return Response(juegos)

5. agregar la nueva ruta en api/urls.py:
  
  from .views import JuegosPopularesAPIView

urlpatterns += [
    path('juegos-populares/', JuegosPopularesAPIView.as_view(), name='api_juegos_populares'),
]

 # puedes probar esta API externa visitando:  http://127.0.0.1:8000/api/juegos-populares/
     debe mostar un JSON con los juegos populares de la API RAWG

	 "cada vez que lo quieran probar deben correr primero: python manage.py runserver "

    #  seguridad en la API REST (Categorias)
    se ha implemento seguridad por autenticación en las rutas de la API REST.
    se activó la siguiente configuración en settings.py:

    REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
esto significa que se le exige al usuario que este autenticado (mediante sesion)

 proteccion explicita en la vista de categorias: en la api/views.py se agrego el permiso de autenticacion directamente en la vista CategoriaListAPIView:

 from rest_framework.permissions import IsAuthenticated

class CategoriaListAPIView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]  # vista protegida

    





