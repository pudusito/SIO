from django.db import models


# El supervisor crea turnos y se lo asocia a la matrona
class Turno(models.Model):
    class Tipo(models.TextChoices):
        DIURNO = 'diurno', 'Diurno'
        VESPERTINO = 'vespertino', 'Vespertino'

    tipo = models.CharField(max_length=30, 
                            choices=Tipo.choices,
                            default=Tipo.DIURNO)
    nombre = models.CharField(max_length=30)
    hora_ingreso = models.TimeField()
    hora_egreso = models.TimeField()


    def __str__(self):
        return f"Turno: {self.nombre} / {self.tipo}"


