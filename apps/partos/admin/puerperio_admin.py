from django.contrib import admin
from ..models import Puerperio

@admin.register(Puerperio)
class PuerperioAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'parto',
        'estado_perine',
        'esterilizacion',
        'revision',
        'inercia_uterina',
        'created_at',
    )

    list_filter = (
        'estado_perine',
        'esterilizacion',
        'revision',
        'inercia_uterina',
        'restos_placenta',
        'trauma',
    )

    search_fields = (
        'parto__id',
        'created_by__username',
    )

    autocomplete_fields = ('parto',)

    readonly_fields = (
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    fieldsets = (
        ('Información del Puerperio', {
            'fields': (
                'parto',
                'estado_perine',
                'esterilizacion',
                'revision',
                'inercia_uterina',
                'restos_placenta',
                'trauma',
                'alteracion_coagulacion',
                'manejo_qirurgico_inercia_ut',
            )
        }),

        ('Registro del Sistema', {
            'fields': (
                'created_at',
                'created_by',
                'updated_at',
                'updated_by',
            ),
            'classes': ('collapse',)
        }),
    )
