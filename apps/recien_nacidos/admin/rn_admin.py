from django.contrib import admin
from ..models.rn import RecienNacido


@admin.register(RecienNacido)
class RecienNacidoAdmin(admin.ModelAdmin):

    list_display = (
        'codigo',
        'nombre_completo_madre',
        'parto',
        'fecha_hora',
        'peso',
        'talla',
        'presentacion_fetal',
        'destino',
        'sexo',
    )

    search_fields = (
        'codigo',
        'nombre_completo_madre',
        'parto__id',
    )

    list_filter = (
        'presentacion_fetal',
        'destino',
        'sexo',
        'fecha_hora',
        'alojamiento_conjunto',
        'apego_canguro',
        'lactante_60',
        'apego_tunel',
        'gases_de_cordon',
    )

    filter_horizontal = (
        'complicaciones_postparto',
        'reanimaciones_neonatales',
    )

    ordering = ('-fecha_hora',)
    list_per_page = 20

    # -------------------------
    # CAMPOS NO EDITABLES
    # -------------------------
    readonly_fields = (
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )

    fieldsets = (
        ("Identificación del RN", {
            "fields": (
                'codigo',
                'fecha_hora',
                'parto',
                'nombre_completo_madre',
                'sexo',
                'destino',
                'destino_rn',
            )
        }),

        ("Medidas Antropométricas", {
            "fields": (
                'peso',
                'talla',
                'perimetro_cefalico',
                'perimetro_toraxico',
                'c_2480',
            )
        }),

        ("Evaluación Apgar", {
            "fields": (
                'apgar_1',
                'apgar_5',
            )
        }),

        ("Presentación y Reanimación", {
            "fields": (
                'presentacion_fetal',
                'complicaciones_postparto',
                'reanimaciones_neonatales',
            )
        }),

        ("Cuidados y Observaciones", {
            "fields": (
                'alojamiento_conjunto',
                'apego_canguro',
                'lactante_60',
                'apego_tunel',
                'gases_de_cordon',
                'observaciones',
            )
        }),

        # -------------------------
        # FIELDSET DE AUDITORÍA (READ-ONLY)
        # -------------------------
        ("Registro del sistema", {
            "fields": (
                'created_by',
                'created_at',
                'updated_by',
                'updated_at',
            ),
            "classes": ("collapse",)
        }),
    )
