from django.contrib import admin
from ..models import Nacionalidad

@admin.register(Nacionalidad)
class nacionalidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)