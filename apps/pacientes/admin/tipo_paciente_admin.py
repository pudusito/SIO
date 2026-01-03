from django.contrib import admin
from ..models import TipoPaciente

@admin.register(TipoPaciente)
class TipoPacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
