from django.contrib import admin
from ..models import TipoAnalgesia

@admin.register(TipoAnalgesia)
class TipoAnalgesiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('nombre',)
