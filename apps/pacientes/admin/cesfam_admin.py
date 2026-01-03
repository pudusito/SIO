from django.contrib import admin
from ..models import Cesfam

@admin.register(Cesfam)
class CesfamAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'comuna',)
    search_fields = ('nombre', 'comuna__nombre',)
    list_filter = ('comuna',)
    ordering = ('nombre', 'comuna__nombre',)  
