from django.shortcuts import render

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

