from django.contrib import admin
from ..models import Parto


@admin.register(Parto)
class PartoAdmin(admin.ModelAdmin):
    list_display = (
    'id',
    'gestacion',
    'created_by',
    'via_nacimiento',
    'estado',
    'created_at',)

    list_filter = (
    'via_nacimiento',
    'estado',
    'tipo_de_ingreso',
    'grupo_robson',)

    search_fields = (
    'gestacion__paciente__identificacion',)



    readonly_fields = ('created_at', 'updated_at', 'updated_by')

    fieldsets = (
        ('Información general', {
            'fields': (
                'created_by',
                'gestacion',
                'estado',
            )
        }),

        ('Datos obstétricos', {
            'fields': (
                'tipo_de_ingreso',
                'grupo_robson',
                'via_nacimiento',
                'posicion',
                'rotura_membrana',
                'tiempo_membrana_rota',
                'tiempo_dilatacion',
                'tiempo_expulsivo',
                'numero_aro',
                'edad_madre',
            )
        }),

        ('Acciones y procesos', {
            'fields': (
                'induccion',
                'aceleracion',
                'oxitocina_profilactica',
                'entrega_placenta',
                'monitor',
                'uso_sala_saip',
                'acompaniante',
                'ttc',
                'tipo_regimen',
                'n_tactos_vaginales',
            )
        }),

        ('Analgesias y complicaciones', {
            'fields': ('complicaciones',)
        }),

        ('Registro del Sistema', {
            'fields': (
                'updated_by',
                'updated_at',
                'observaciones',
            ),
            'classes': ('collapse',)
        }),
    )