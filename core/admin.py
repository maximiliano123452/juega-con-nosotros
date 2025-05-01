from django.contrib import admin
from core.models import Categoria, Juego, Usuario, Favorito, Contacto
from django.utils import timezone

admin.site.register(Categoria)
admin.site.register(Juego)
admin.site.register(Usuario)
admin.site.register(Favorito)

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'fecha_creacion', 'leido', 'mensaje_corto')
    list_filter = ('leido', 'fecha_creacion')
    search_fields = ('nombre', 'email', 'mensaje')
    date_hierarchy = 'fecha_creacion'
    list_editable = ('leido',)  
    actions = ['marcar_como_leido']

    fieldsets = (
        ('Información del contacto', {
            'fields': ('nombre', 'email', 'fecha_creacion')
        }),
        ('Mensaje', {
            'fields': ('mensaje', 'leido', 'respuesta'),
            'classes': ('wide',),
        }),
    )

    readonly_fields = ('fecha_creacion',) 

    def mensaje_corto(self, obj):
        return obj.mensaje[:50] + '...' if len(obj.mensaje) > 50 else obj.mensaje
    mensaje_corto.short_description = 'Mensaje (resumen)'

    def marcar_como_leido(self, request, queryset):
        updated = queryset.update(leido=True)
        self.message_user(request, f"{updated} mensajes marcados como leídos")
    marcar_como_leido.short_description = 'Marcar como leído'