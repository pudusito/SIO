from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from .gestacion import Gestacion
from ..fields import OrderField

class Test(models.Model):
    
    class Resultado(models.TextChoices):
        REACTIVO = "positivo", "Reactivo"
        NO_REACTIVO = "negativo", "No Reactivo"
    
    class LugarToma(models.TextChoices):
        PREPARTO = 'preparto', 'Preparto'
        SALA_PARTO = 'sala_parto', 'Sala de Partos'
        URGENCIA = 'urgencia', 'Urgencias'
            
    
    gestacion = models.ForeignKey(Gestacion, on_delete=models.CASCADE, 
                                  related_name="%(class)s")
    resultado = models.CharField(max_length=15,
                                 choices=Resultado.choices,
                                 default=Resultado.NO_REACTIVO)
    fecha_toma = models.DateField(help_text="Fecha en la que se tomo el examen")
    
    # NO VA EN EL FORMULARIO
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    lugar_toma = models.CharField(max_length=12,
                                  choices=LugarToma.choices,
                                  default=LugarToma.PREPARTO)
    antibiotico = models.BooleanField(default=False)
    durante_parto = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True, max_length=1000)

    # NO VA EN EL FORMULARIO
    orden = OrderField(for_fields=['gestacion'])


    class Meta:
        abstract = True


class TestVih(Test):
    class Trimestre(models.TextChoices):
        PRIMERO = '1', 'Primer Trimestre (0-12 semanas)'
        SEGUNDO = '2', 'Segundo Trimestre (13-27 semanas)'
        TERCERO = '3', 'Tercer Trimestre (28-40 semanas)'


    n_aro = models.PositiveIntegerField()
    trimestre = models.CharField(max_length=20, 
                                 choices=Trimestre.choices,
                                 default=Trimestre.PRIMERO)




class TestSgb(Test):
    pass



class TestVdrl(Test):
    pass

class TestHepatitisB(Test):
    derivacion_especialista = models.BooleanField(default=False)

