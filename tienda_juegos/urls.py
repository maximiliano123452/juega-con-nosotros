from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls')),         # ruta principal
    path('core/', include('core.urls')),   # ruta para la app core
    path('api/', include('api.urls')),     # nueva ruta para la API REST
]

# Esto permite servir archivos estaticos durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])


