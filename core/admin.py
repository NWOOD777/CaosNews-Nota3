from django.contrib import admin
from .models import *
from admin_confirm import AdminConfirmMixin

class PeriodistaAdmin(AdminConfirmMixin, admin.ModelAdmin):
    confirm_change = True
    confirmation_fields = ['rut', 'nombre','apellido','edad','correo','imagen_perfil']

class NoticiaAdmin(AdminConfirmMixin, admin.ModelAdmin):
    confirm_change = True
    confirmation_fields = ['titulo', 'descripcion','periodista','categoria']

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Periodista, PeriodistaAdmin)
admin.site.register(Noticia, NoticiaAdmin)