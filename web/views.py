from django.shortcuts import render

# Vistas principales
def index(request):
    return render(request, 'web/index.html')

def login(request):
    return render(request, 'web/login.html')

def registro(request):
    return render(request, 'web/registro.html')

def perfil(request):
    return render(request, 'web/perfil.html')

def recuperar(request):
    return render(request, 'web/recuperar.html')

def contacto(request):
    return render(request, 'web/contacto.html')

def carrito(request):
    return render(request, 'web/carrito.html')

# Vistas de Categorías
def categoria_carreras(request):
    return render(request, 'categorias/carreras.html')

def categoria_cozy(request):
    return render(request, 'categorias/cozy.html')

def categoria_mundoabierto(request):
    return render(request, 'categorias/mundoabierto.html')

def categoria_shooters(request):
    return render(request, 'categorias/shooters.html')

def categoria_terror(request):
    return render(request, 'categorias/terror.html')

# Vistas de Juegos - Carreras
def crashteamracing(request):
    return render(request, 'juegos/carreras/crashteamracing.html')

def mariokart8deluxe(request):
    return render(request, 'juegos/carreras/mariokart8deluxe.html')

# Vistas de Juegos - Cozy
def stardewvalley(request):
    return render(request, 'juegos/cozy/stardewvalley.html')

def spiritfarer(request):
    return render(request, 'juegos/cozy/spiritfarer.html')

# Vistas de Juegos - Mundo Abierto
def cyberpunk2077(request):
    return render(request, 'juegos/mundoabierto/cyberpunk2077.html')

def zeldatotk(request):
    return render(request, 'juegos/mundoabierto/zeldatotk.html')

# Vistas de Juegos - Shooters
def doometernal(request):
    return render(request, 'juegos/shooters/doometernal.html')

def splatoon2(request):
    return render(request, 'juegos/shooters/splatoon2.html')

# Vistas de Juegos - Terror
def alanwake2(request):
    return render(request, 'juegos/terror/alanwake2.html')

def residentevil4remake(request):
    return render(request, 'juegos/terror/residentevil4remake.html')



