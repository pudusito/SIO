from django.contrib import admin
from ..models.detalle_rn import ComplicacionPostParto, PresentacionFetal, ReanimacionNeonatal



# complicaciones post parto
@admin.register(ComplicacionPostParto)
class ComplicacionPostPartoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

# presentacion fetal
@admin.register(PresentacionFetal)
class PresentacionFetalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

# reanimacion neonatal
@admin.register(ReanimacionNeonatal)
class ReanimacionNeonatalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'descripcion')
    search_fields = ('nombre',)
    list_filter = ('tipo',)