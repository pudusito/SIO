from django.contrib import admin
from ..models.vacunacion import Vacunacion

@admin.register(Vacunacion)
class VacunacionAdmin(admin.ModelAdmin):

    list_display = ('recien_nacido','profesional','fecha','reaccion_adversa',)

    search_fields = ('recien_nacido__nombre_completo', 'recien_nacido__codigo','profesional__nombre', 'profesional__apellido','reaccion_adversa',)

    list_filter = ('fecha','profesional','reaccion_adversa',)

    ordering = ('-fecha',)
    list_per_page = 25

    fieldsets = (
        ('Información del RN', {
            'fields': (
                'recien_nacido',
            )
        }),

        ('Aplicación de Vacuna', {
            'fields': (
                'profesional',
                'fecha',
                'reaccion_adversa',
            )
        }),
    )
