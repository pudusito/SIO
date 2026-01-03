from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from ..models import Paciente

@admin.register(Paciente)
class PacienteAdmin(SimpleHistoryAdmin):

    list_display = (
        'documento',
        'identificacion',
        'obtener_nombre_completo',
        'tipo',
        'nacionalidad',
        'comuna',
        'cesfam',
        'telefono',
        'fecha_nacimiento',
        'descapacitado',
    )
    history_list_display = ['status']

 
    search_fields = (
        'identificacion',
        'nombre',
        'primer_apellido',
        'segundo_apellido',
        'telefono',
        'comuna__nombre',
        'cesfam__nombre',
    )

    list_filter = (
        'tipo',
        'nacionalidad',
        'comuna',
        'cesfam',
        'descapacitado',
        'pueblo_originario',
        'privada_de_libertad',
        'transexual',
        'plan_de_parto',
        'visita_guiada',
        'actividad',
        'fecha_nacimiento',
    )

    ordering = ('primer_apellido', 'segundo_apellido', 'nombre')
    list_per_page = 20

    # listito ahi me estaba dando cualquier problema con el cambio de fecha a created y updaed
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Identificación', {
            'fields': ('documento', 'identificacion')
        }),

        ('Datos Personales', {
            'fields': (
                'nombre', 'primer_apellido', 'segundo_apellido',
                'fecha_nacimiento', 'nacionalidad',
                'comuna', 'cesfam', 'direccion', 'telefono', "tipo"
            )
        }),

        ('Situación Especial', {
            'fields': (
                'descapacitado',
                'pueblo_originario',
                'privada_de_libertad',
                'transexual',
            )
        }),

        ('Parto y Planificación', {
            'fields': ('plan_de_parto', 'visita_guiada')
        }),

        ('Datos Clínicos', {
            'fields': ('peso', 'altura', 'actividad')
        }),

        ('Registro del Sistema', {
            'fields': ('created_by', 'created_at', 'updated_by', 'updated_at'),
            'classes': ('collapse',)
        }),
    )



