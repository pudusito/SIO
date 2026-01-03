from django.contrib import admin
from ..models import Gestacion


@admin.register(Gestacion)
class GestacionAdmin(admin.ModelAdmin):

    list_display = (
        'paciente',
        'numero_gestacion',
        'riesgo',
        'estado',
        'multiple',
        'numero_fetos',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'paciente__nombre',
        'paciente__primer_apellido',
        'paciente__segundo_apellido',
        'paciente__identificacion',
    )

    list_filter = (
        'riesgo',
        'estado',
        'multiple',
        'enfermedad_cardiaca',
        'hipertension',
        'diabetes',
        'created_at',
    )

    ordering = ('-created_at',)
    list_per_page = 20

    readonly_fields = (
        'created_at',
        'updated_at',
        'fecha_inicio_gestacion',
    )

    fieldsets = (
        ('Información del Paciente', {
            'fields': (
                'paciente',
                'numero_gestacion',
            )
        }),

        ('Detalles Clínicos', {
            'fields': (
                'riesgo',
                'estado',
                'multiple',
                'numero_fetos',
                'enfermedad_cardiaca',
                'hipertension',
                'diabetes',
            )
        }),

        ('Método de Datación', {
            'fields': (
                'origen_datacion',
                'fur',
                'fecha_eco',
                'semanas_eco',
                'dias_eco',
                'fecha_inicio_gestacion',
            )
        }),

        ('Registro del Sistema', {
            'fields': (
                'created_by',
                'created_at',
                'updated_by',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
