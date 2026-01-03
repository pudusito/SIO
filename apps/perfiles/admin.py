from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    MatronaPerfil, Turno, SupervisorPerfil, Usuario
)

# INLINES
class MatronaPerfilInline(admin.StackedInline):
    model = MatronaPerfil
    extra = 0
    verbose_name = "Perfil Matrona"


class SupervisorPerfilInline(admin.StackedInline):
    model = SupervisorPerfil
    extra = 0
    verbose_name = "Perfil Supervisor"


# REGISTRO DE MODELOS EN EL ADMIN
@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('es_matrona', 'es_supervisor')
    inlines = (MatronaPerfilInline, SupervisorPerfilInline)
    fieldsets = BaseUserAdmin.fieldsets + (('Tipo de Usuario', {'fields': ('es_matrona', 'es_supervisor')}), )


@admin.register(MatronaPerfil)
class MatronaAdmin(admin.ModelAdmin):
    pass



@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    pass


@admin.register(SupervisorPerfil)
class SupervisorAdmin(admin.ModelAdmin):
    pass