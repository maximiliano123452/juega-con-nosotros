from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls')),  # Ruta principal apunta a tu app web
    path('core/', include('core.urls')),  # Ruta para la app core
    #path('registro/', include('web.urls')), 
]

# ✅ Esto permite servir archivos estáticos durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

