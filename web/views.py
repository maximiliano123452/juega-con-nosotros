from django.shortcuts import render

# Vistas principales
def index(request):
    return render(request, 'web/index.html', {
        "categorias": CATEGORIAS
    })

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
    juegos_categoria = {k: v for k, v in JUEGOS.items() if v["categoria"] == "carreras"}
    return render(request, 'categorias/carreras.html', {
        "categoria": CATEGORIAS["carreras"],
        "juegos": juegos_categoria
    })

def categoria_cozy(request):
    juegos_categoria = {k: v for k, v in JUEGOS.items() if v["categoria"] == "cozy"}
    return render(request, 'categorias/cozy.html', {
        "categoria": CATEGORIAS["cozy"],
        "juegos": juegos_categoria
    })

def categoria_mundoabierto(request):
    juegos_categoria = {k: v for k, v in JUEGOS.items() if v["categoria"].replace(" ", "").lower() == CATEGORIAS[3]["nombre"].replace(" ", "").lower()}
    return render(request, 'categorias/mundoabierto.html', {
        "categoria": CATEGORIAS["mundoabierto"],
        "juegos": juegos_categoria
    })


def categoria_shooters(request):
    juegos_categoria = {k: v for k, v in JUEGOS.items() if v["categoria"] == "shooters"}
    return render(request, 'categorias/shooters.html', {
        "categoria": CATEGORIAS["shooters"],
        "juegos": juegos_categoria
    })

def categoria_terror(request):
    juegos_categoria = {k: v for k, v in JUEGOS.items() if v["categoria"] == "terror"}
    return render(request, 'categorias/terror.html', {
        "categoria": CATEGORIAS["terror"],
        "juegos": juegos_categoria
    })

# Vista dinámica para mostrar cualquier categoría
def subcategoria(request, categoria_id):
    categoria = CATEGORIAS.get(categoria_id)  # Usar categoria_id para obtener la categoría desde el diccionario
    juegos_categoria = {k: v for k, v in JUEGOS.items() if v["categoria"] == categoria["nombre"].lower()}
    return render(request, 'web/subcategorias.html', {
        'categoria': categoria,
        'juegos': juegos_categoria
    })

# Diccionario de datos de categorias 

CATEGORIAS = {
    1: {
        "nombre": "Carreras",
        "titulo": "Carreras",
        "lema": "🏎️ Carreras: La velocidad lo es todo.",
        "descripcion": "Compite en emocionantes circuitos, domina curvas cerradas y deja atrás a tus rivales en intensas carreras llenas de adrenalina.",
        "imagen": "/static/img/carreras.jpg"
    },
    2: {
        "nombre": "Cozy",
        "titulo": "Cozy",
        "lema": "☕ Cozy: Relájate y disfruta.",
        "descripcion": "Juegos tranquilos con ambientaciones acogedoras, mecánicas relajantes y un ritmo pausado para desconectar del estrés.",
        "imagen": "/static/img/cozy.jpg"
    },
    3: {
        "nombre": "mundoabierto",
        "titulo": "Mundo Abierto",
        "lema": "🌍 Mundo Abierto: Explora sin límites.",
        "descripcion": "Aventúrate en vastos mundos llenos de secretos, desafíos y personajes inolvidables. La historia la escribes tú.",
        "imagen": "/static/img/mundo-abierto.jpg"
    },
    4: {
        "nombre": "Shooters",
        "titulo": "Shooters",
        "lema": "🎯 Shooters: Acción sin descanso.",
        "descripcion": "  Enfréntate a enemigos en intensos tiroteos, ya sea en combates tácticos, arenas frenéticas o guerras épicas.",
        "imagen": "/static/img/shooters.jpg"
    },
    5: {
        "nombre": "Terror",
        "titulo": "Terror",
        "lema": "👻 Terror: Sobrevive a la pesadilla.",
        "descripcion": "Sumérgete en historias escalofriantes, evade horrores indescriptibles y enfrenta el miedo en cada sombra.",
        "imagen": "/static/img/terror.jpg"
    },
}



# Vista dinámica para mostrar cualquier juego
def detalle_juego(request, juego_id):
    juego = JUEGOS.get(int(juego_id))
    return render(request, 'web/detalle.html', {'juego': juego})



# Diccionario con los datos de los juegos

JUEGOS = {
    1: {
        "titulo": "Crash Team Racing Nitro-Fueled",
        "plataformas": "PS4, Xbox One, Nintendo Switch, PC",
        "descripcion": "Revive la emoción de las carreras arcade con Crash y sus amigos. Derrapa a toda velocidad, usa ítems locos y domina los circuitos llenos de obstáculos en este vibrante remake del clásico de PlayStation.",
        "precio": "20.000",
        "imagen": "/static/img/crashteamracing.jpg",
        "categoria": "carreras",
    },
    2: {
        "titulo": "Mario Kart 8 Deluxe",
        "plataformas": "Nintendo Switch",
        "descripcion": "Compite en pistas alocadas, usa ítems estratégicos y disfruta de la mejor experiencia multijugador de carreras con Mario y sus amigos.",
        "precio": "49.990",
        "imagen": "/static/img/mariokart8deluxe.jpg",
        "categoria": "carreras",
    },
    3: {
        "titulo": "Stardew Valley",
        "plataformas": "PS4, Xbox One, Nintendo Switch, PC",
        "descripcion": "Crea la granja de tus sueños en este relajante juego de simulación.",
        "precio": "14.990",
        "imagen": "/static/img/stardewvalley.jpg",
        "categoria": "cozy",
    },
    4: {
        "titulo": "Spiritfarer",
        "plataformas": "PS4, Xbox One, Nintendo Switch, PC",
        "descripcion": "Un conmovedor juego sobre la muerte y la amistad.",
        "precio": "29.990",
        "imagen": "/static/img/spiritfarer.jpg",
        "categoria": "cozy",
    },
    5: {
        "titulo": "Cyberpunk 2077",
        "plataformas": "PS4, Xbox One, PC",
        "descripcion": "Un RPG de mundo abierto ambientado en el futuro distópico de Night City.",
        "precio": "59.990",
        "imagen": "/static/img/cyberpunk2077.jpg",
        "categoria": "mundoabierto",
    },
    6: {
        "titulo": "The Legend of Zelda: Tears of the Kingdom",
        "plataformas": "Nintendo Switch",
        "descripcion": "Explora Hyrule y descubre sus secretos en esta épica secuela de Breath of the Wild.",
        "precio": "69.990",
        "imagen": "/static/img/zeldatotk.jpg",
        "categoria": "mundoabierto",
    },
    7: {
        "titulo": "DOOM Eternal",
        "plataformas": "PS4, Xbox One, PC",
        "descripcion": "Enfréntate a hordas de demonios en este frenético shooter en primera persona.",
        "precio": "39.990",
        "imagen": "/static/img/doometernal.jpg",
        "categoria": "shooters",
    },
    8: {
        "titulo": "Splatoon 2",
        "plataformas": "Nintendo Switch",
        "descripcion": "Disfruta de emocionantes batallas de pintura multijugador.",
        "precio": "49.990",
        "imagen": "/static/img/splatoon2.jpg",
        "categoria": "shooters",
    },
    9: {
        "titulo": "Alan Wake 2",
        "plataformas": "PS5, Xbox Series X/S, PC",
        "descripcion": "Una oscura historia de terror psicológico que desafía la realidad.",
        "precio": "59.999",
        "imagen": "/static/img/alanwake2.jpg",
        "categoria": "terror",
    },
    10: {
        "titulo": "Resident Evil 4 Remake",
        "plataformas": "PS4, PS5, Xbox Series X/S, PC",
        "descripcion": "Revive el clásico de terror con gráficos y jugabilidad mejorados.",
        "precio": "59.999",
        "imagen": "/static/img/residentevil4remake.jpg",
        "categoria": "terror",
    },
}

