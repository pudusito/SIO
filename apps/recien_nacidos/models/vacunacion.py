from django.db import models
from django.conf import settings
from .rn import RecienNacido
from apps.partos.models import Profesional

# NO TIENE FORMULARIO ESTE MODELO
class TipoVacuna(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)



# ESTE SI TIENE FORMULARIO
class Vacunacion(models.Model):
    recien_nacido = models.ForeignKey(RecienNacido, on_delete=models.CASCADE, related_name='vacunaciones')
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name='vacunaciones')
    fecha = models.DateField()
    reaccion_adversa = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoVacuna, on_delete=models.PROTECT, related_name='vacunas')
    
    # ESTOS CAMPOS NO VAN EN EL FORMULARIO
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='vacunaciones', null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='vacunaciones_actualizacion', null=True)