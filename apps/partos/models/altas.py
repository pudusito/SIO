# Lo coloco en esta app pq son las altas tanto de los recien nacidos como la madre
from django.db import models
from django.conf import settings
from apps.pacientes.models import Paciente
from apps.recien_nacidos.models import RecienNacido



class AltaMadre(models.Model):
    class CondicionEgreso(models.TextChoices):
        ESTABLE = 'estable', 'Estable (Domicilio)'
        OBSERVACION = 'observacion', 'Estable con Recomendaciones (Observación)'
        COMPLICACION_MENOR = 'compl_menor', 'Complicación Menor'
        COMPLICACION_MAYOR = 'compl_mayor', 'Complicación Mayor (Pendiente de manejo)'
    
        # Destinos
        TRASLADO_HOSP = 'traslado_hosp', 'Traslado a Otra Unidad/Hospital'
        FALLECIDA = 'fallecida', 'Fallecida'
    
    madre = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='altas')
    fecha_alta = models.DateTimeField(auto_now_add=True)
    condicion_egreso = models.CharField(max_length=30, 
                                        choices=CondicionEgreso.choices,
                                        default=CondicionEgreso.ESTABLE)
    dx_egreso_madre = models.TextField()
    epicrisis = models.TextField()
    medico_alta = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='altas_madre')



class AltaRN(models.Model):
    class CondicionEgreso(models.TextChoices):
        
        ALTA_DOMICILIO = 'domicilio', 'Estable (Alta a Domicilio)'
        ALTA_PREMATURO = 'domicilio_pre', 'Alta a Domicilio (Bajo Peso/Prematuro Estabilizado)'
        HOSP_INTERMEDIO = 'hosp_interm', 'Hospitalización Intermedia (Pediátrica)'
        HOSP_CRITICO = 'hosp_critico', 'Hospitalización Crítica (UCI/UTI Neonatal)'
        
        TRASLADO_OTRO_CENTRO = 'traslado_centro', 'Traslado a Otro Centro Médico'
        FALLECIDO = 'fallecido', 'Fallecido'
        
        ALTA_VOLUNTARIA = 'alta_voluntaria', 'Alta Voluntaria'
        PENDIENTE_INFORME = 'pendiente_inf', 'Pendiente de Informe/Resultados de Tamizaje'

    rn = models.ForeignKey(RecienNacido, on_delete=models.CASCADE, related_name='altas')
    fecha_alta = models.DateTimeField(auto_now_add=True)
    condicion_egreso = models.CharField(max_length=30, 
                                        choices=CondicionEgreso.choices,
                                        default=CondicionEgreso.ALTA_DOMICILIO)
    peso = models.PositiveIntegerField()
    dx_egreso_rn = models.TextField()
    indicaciones = models.TextField()
    medico_alta = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='altas_rn')
