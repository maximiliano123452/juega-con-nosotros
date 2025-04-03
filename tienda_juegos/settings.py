from pathlib import Path
import os

# BASE_DIR es la raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta (para desarrollo está bien)
SECRET_KEY = 'django-insecure-vw$(fv*vnm_$)yixzaz7wl0re8%cqo54x_n-14%klu5vx##h_v'

# Activa modo desarrollo (¡no para producción!)
DEBUG = True

ALLOWED_HOSTS = []

# Apps instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web',  # Tu app principal
]

# Middlewares que usa Django
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL principal
ROOT_URLCONF = 'tienda_juegos.urls'

# Configuración de plantillas HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Django buscará plantillas en templates/ dentro de las apps
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Aplicación WSGI
WSGI_APPLICATION = 'tienda_juegos.wsgi.application'

# Configuración de base de datos (por defecto SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuración regional
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# ✅ Archivos estáticos (CSS, JS, imágenes)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'web/static'),
]

# ✅ Archivos subidos por usuarios (opcional)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Por ahora no hay configuración de correo ni autenticación extra



