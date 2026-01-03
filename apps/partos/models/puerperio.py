from django.db import models
from django.conf import settings
from .parto import Parto

# Info ingresada despues del trabajo de parto
class Puerperio(models.Model):
    class EstadoPerine(models.TextChoices):
        INDEMNE = 'indemne', 'Indemne'
        DESGARRO_G1 = 'g1', 'Desgarro G1'
        DESGARRO_G2 = 'g2', 'Desgarro G2'
        DESGARRO_G3A = 'g3a', 'Desgarro G3 A'
        DESGARRO_G3B = 'g3b', 'Desgarro G3 B'
        DESGARRO_G3C = 'g3c', 'Desgarro G3 C'
        DESGARRO_G4 = 'g4', 'Desgarro G4'
        FISURA = 'fisura', 'Fisura'
        EPISIOTOMIA ='episiotomia', 'Episiotomia'

    estado_perine = models.CharField(max_length=30,
                                choices=EstadoPerine.choices,
                                default=EstadoPerine.INDEMNE)
    
    esterilizacion = models.BooleanField(default=False)
    revision = models.BooleanField(default=False)
    inercia_uterina = models.BooleanField(default=False)
    restos_placenta = models.BooleanField(default=False)
    trauma = models.BooleanField(default=False)
    alteracion_coagulacion = models.BooleanField(default=False)
    manejo_qirurgico_inercia_ut = models.BooleanField(default=False)
    # NO VAN EN EL FORMULARIO
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='puerperios', null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='puerperios_actualizados', null=True)
    # ESTE SI VA, ES UN SELECT
    parto = models.OneToOneField(Parto, on_delete=models.PROTECT, related_name='puerperio')

    def __str__(self):
        return f"Puerperio de Parto {self.parto.pk}"


