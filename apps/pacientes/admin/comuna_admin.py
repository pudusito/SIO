from django.contrib import admin
from ..models import Comuna

@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)
