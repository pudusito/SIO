from django.db import models
from django.conf import settings
from .parto import Parto

# No la dejo como M2M pq cada analgesia que se le suministra no es solo una relacion si no
# que tmb se detalla mas info y tipo

# ESTE MODELO NO TIENE FORMULARIO
class TipoAnalgesia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    '''
    Histerectomía Obstétrica	
    Tranfusión Sanguínea	
    Anestesia Neuroaxial	
    Óxido nitroso	
    Analgesia endovenosa	
    General	Local	 
    Analgesia NO farmac. 	
    Balón Kinesico	
    Lenteja de Parto	
    Rebozo	
    Aromaterapia	
    Anest. Peridural Solicitada por paciente	
    Anest. Peridural indicada por médico GO	Anest. 
    Peridural administrada	
    Tiempo de espera entre indicación médica y administración de Anest. Peridural
    '''
    def __str__(self):
            return self.nombre


class AnalgesiaParto(models.Model):
    parto = models.ForeignKey(
        Parto,
        on_delete=models.CASCADE,
        related_name='analgesias'
    )

    tipo = models.ForeignKey(
        TipoAnalgesia,
        on_delete=models.PROTECT
    )

    solicitada = models.BooleanField(default=False)
    indicada = models.BooleanField(default=False)
    administrada = models.BooleanField(default=False)

    tiempo_espera_minutos = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Tiempo entre indicación y administración"
    )

    dosis = models.CharField(max_length=10)

    notas = models.TextField(blank=True, null=True)

    # NO VAN EN EL FORMULARIO
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='analgesias', null=True)


    class Meta:
         unique_together = ('parto', 'tipo')
    def __str__(self):
        return f"{self.tipo.nombre} ({self.parto.id})"

