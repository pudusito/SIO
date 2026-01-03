from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from simple_history.models import HistoricalRecords

from .detalle_rn import (ComplicacionPostParto, PresentacionFetal, ReanimacionNeonatal)
from apps.partos.models import Parto

class RecienNacido(models.Model):

    class Sexo(models.TextChoices):
        MASCULINO = 'm', 'Masculino'
        FEMENINO = 'f', 'Femenino'
        OTRO = 'o', 'Otro'

    class Destino(models.TextChoices):
        ALOJAMIENTO = 'alojamiento', 'Alojamiento conjunto'
        UCI = 'uci', 'UCI Neonatal'
        UTI = 'uti', 'UTI Neonatal'
        FALLECE = 'fallecido', 'Fallecido'



    # ForeignKey ya que asi podemos asociar uno o mas bebes al mismo parto o diferentes partos, ya que de 1 parto pueden haber mas de 1
    # bebe asociado porque el parto pudo ser multiple
    parto = models.ForeignKey(Parto, on_delete=models.PROTECT, related_name='rns')
    # NO VAN EN EL FORMULARIO
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='rns', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='rns_actualizados', null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    presentacion_fetal = models.ForeignKey(PresentacionFetal, on_delete=models.PROTECT, related_name='rns')
    complicaciones_postparto = models.ManyToManyField(ComplicacionPostParto, related_name='rns', blank=True)
    reanimaciones_neonatales = models.ManyToManyField(ReanimacionNeonatal, related_name='rns', blank=True)
    fecha_hora = models.DateTimeField()
    nombre_completo_madre = models.CharField(max_length=150, blank=True)
    peso = models.PositiveIntegerField() # Se mide en gramos asi que es un valor numerico entero
    talla = models.DecimalField(max_digits=4, decimal_places=1)
    apgar_1 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    apgar_5 = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    codigo = models.CharField(max_length=20, unique=True)
    perimetro_cefalico = models.DecimalField(max_digits=4, decimal_places=1)
    perimetro_toraxico = models.DecimalField(max_digits=4, decimal_places=1)
    c_2480 = models.PositiveSmallIntegerField()
    destino_rn = models.CharField(max_length=100, blank=True)
    observaciones = models.TextField(blank=True)
    alojamiento_conjunto = models.BooleanField()
    apego_canguro = models.BooleanField()
    lactante_60 = models.BooleanField()
    apego_tunel = models.BooleanField()
    gases_de_cordon = models.BooleanField()
    destino = models.CharField(max_length=50, 
                               choices=Destino.choices,
                               default=Destino.ALOJAMIENTO)
    sexo = models.CharField(
        max_length=10,
        choices=Sexo.choices,
        default=Sexo.OTRO
    )
    
    history = HistoricalRecords()
    
    def save(self, *args, **kwargs):
        if not self.nombre_completo_madre:
            parto = Parto.objects.select_related('gestacion__paciente').get(pk=self.parto.pk)
            madre = parto.gestacion.paciente
            self.nombre_completo_madre = madre.obtener_nombre_completo()
        super().save()




'''
B. Validaciones de consistencia lógica

Si Apgar_1 < 7 → reanimaciones_neonatales no debe estar vacío.

Si gases_de_cordon = True → asegurarse de registrar el resultado en otro modelo.

Si alojamiento_conjunto = True → RN no puede estar en UCI/UTI.

Si peso < 2500 g o EG < 37 → sugerir marcar como prematuro.

Presentación fetal debe ser consistente con el parto.

No permitir duplicados del mismo bebé (por código + parto).

Si RN fallece → destino debe ser “fallecido” y registrar fecha/hora.



'''